from __future__ import annotations

import sqlite3
import time
import uuid
from contextvars import ContextVar
from pathlib import Path

from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor, SpanExporter, SpanExportResult

from rag_helper import RAGBase

CURRENT_RUN_ID: ContextVar[str | None] = ContextVar('current_run_id', default=None)


def span_duration_ms(span: ReadableSpan) -> float:
    return (span.end_time - span.start_time) / 1_000_000


class SQLiteSpanExporter(SpanExporter):
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS spans (
                trace_id TEXT,
                span_id TEXT,
                parent_id TEXT,
                run_id TEXT,
                name TEXT,
                start_time INTEGER,
                end_time INTEGER,
                duration_ms REAL,
                input_tokens INTEGER,
                output_tokens INTEGER,
                cost REAL
            )
            '''
        )
        self.conn.commit()

    def export(self, spans: list[ReadableSpan]) -> SpanExportResult:
        rows = []
        for span in spans:
            attrs = span.attributes or {}
            parent_id = None
            if span.parent is not None:
                parent_id = format(span.parent.span_id, '016x')

            rows.append(
                (
                    format(span.context.trace_id, '032x'),
                    format(span.context.span_id, '016x'),
                    parent_id,
                    attrs.get('run_id'),
                    span.name,
                    span.start_time,
                    span.end_time,
                    span_duration_ms(span),
                    attrs.get('input_tokens'),
                    attrs.get('output_tokens'),
                    attrs.get('cost'),
                )
            )

        self.conn.executemany(
            '''
            INSERT INTO spans (
                trace_id, span_id, parent_id, run_id, name, start_time, end_time,
                duration_ms, input_tokens, output_tokens, cost
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            rows,
        )
        self.conn.commit()
        return SpanExportResult.SUCCESS

    def shutdown(self) -> None:
        self.conn.close()


class CollectingSpanExporter(SpanExporter):
    def __init__(self):
        self.spans: list[ReadableSpan] = []

    def export(self, spans: list[ReadableSpan]) -> SpanExportResult:
        self.spans.extend(spans)
        return SpanExportResult.SUCCESS

    def clear(self) -> None:
        self.spans.clear()


def build_tracer_provider(*exporters: SpanExporter) -> TracerProvider:
    provider = TracerProvider()
    for exporter in exporters:
        provider.add_span_processor(SimpleSpanProcessor(exporter))
    return provider


class RAGTraced(RAGBase):
    def __init__(self, *args, tracer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.tracer = tracer

    def search(self, query: str, num_results: int = 5) -> list[dict]:
        with self.tracer.start_as_current_span('search') as span:
            run_id = CURRENT_RUN_ID.get()
            if run_id:
                span.set_attribute('run_id', run_id)
            span.set_attribute('query_length', len(query))
            span.set_attribute('num_results', num_results)
            results = super().search(query, num_results=num_results)
            span.set_attribute('search_result_count', len(results))
            return results

    def llm(self, prompt: str) -> dict:
        with self.tracer.start_as_current_span('llm') as span:
            run_id = CURRENT_RUN_ID.get()
            if run_id:
                span.set_attribute('run_id', run_id)
            span.set_attribute('prompt_length', len(prompt))
            started = time.perf_counter()
            result = super().llm(prompt)
            elapsed_ms = (time.perf_counter() - started) * 1000
            span.set_attribute('provider', result['provider'])
            span.set_attribute('model', result['model'])
            span.set_attribute('input_tokens', result['input_tokens'])
            span.set_attribute('output_tokens', result['output_tokens'])
            span.set_attribute('cost', result['cost'])
            span.set_attribute('duration_ms_local', elapsed_ms)
            return result

    def rag(self, query: str) -> dict:
        run_id = str(uuid.uuid4())
        token = CURRENT_RUN_ID.set(run_id)
        try:
            with self.tracer.start_as_current_span('rag') as span:
                span.set_attribute('run_id', run_id)
                span.set_attribute('query_length', len(query))
                results = self.search(query)
                prompt = self.build_prompt(query, results)
                answer = self.llm(prompt)
                span.set_attribute('search_result_count', len(results))
                span.set_attribute('input_tokens', answer['input_tokens'])
                span.set_attribute('output_tokens', answer['output_tokens'])
                span.set_attribute('cost', answer['cost'])
                return {
                    'run_id': run_id,
                    'query': query,
                    'search_results': results,
                    'prompt': prompt,
                    'answer': answer['text'],
                    'input_tokens': answer['input_tokens'],
                    'output_tokens': answer['output_tokens'],
                    'cost': answer['cost'],
                    'model': answer['model'],
                    'provider': answer['provider'],
                }
        finally:
            CURRENT_RUN_ID.reset(token)


def console_exporter() -> ConsoleSpanExporter:
    return ConsoleSpanExporter()
