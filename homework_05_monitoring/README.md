# Homework 5: Monitoring

This Week 5 workspace instruments a simple RAG system with OpenTelemetry, exports spans to the console and SQLite, and analyzes trace data for the LLM Zoomcamp 2026 Homework 5 questions.

## Objective

- Load the 72 lesson pages from the pinned course commit `8c1834d`
- Build a simple `minsearch` text index
- Run a small RAG pipeline through Qwen
- Capture spans for `rag`, `search`, and `llm`
- Persist finished spans to `traces.db`
- Analyze token usage and span durations for the homework questions

## Setup

```powershell
cd homework_05_monitoring
uv sync
```

The code uses the existing Qwen/OpenAI-compatible configuration if present:

- `QWEN_API_KEY`
- `QWEN_BASE_URL`
- `QWEN_MODEL`

If `QWEN_BASE_URL` or `QWEN_MODEL` are not set locally, the helper falls back to:

- base URL: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
- model: `qwen-plus`

## Run

```powershell
.\.venv\Scripts\jupyter-notebook.exe homework_05_monitoring.ipynb
```

Optional scripts:

```powershell
.\.venv\Scripts\python.exe starter.py
.\.venv\Scripts\python.exe analyze_traces.py
```

## Notebook Sections

1. Setup
2. Starter RAG
3. OpenTelemetry tracing
4. Console span export
5. Token attributes
6. SQLite span exporter
7. Four-run trace collection
8. SQLite analysis
9. Final answers

## Notes

- `traces.db` is created locally and ignored by Git.
- No Docker, Kestra, Postgres, or Grafana is required.
- Do not commit `.env` or any secret values.
