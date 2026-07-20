from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

import logfire

from agent import FINAL_QUERY, load_env
from main import build_agent_and_deps


def run_agent(question: str = FINAL_QUERY) -> dict:
    cfg = load_env()
    if not cfg['logfire_token']:
        raise RuntimeError('LOGFIRE_TOKEN is not available in the environment.')

    logfire.configure(
        send_to_logfire='if-token-present',
        token=cfg['logfire_token'],
        service_name='workshop_dlt_agent',
        base_url=cfg['logfire_base_url'],
        console=False,
    )
    logfire.instrument_pydantic_ai()

    started_at = datetime.now(tz=UTC)
    agent, deps, documents = build_agent_and_deps()
    result = agent.run_sync(question, deps=deps)
    finished_at = datetime.now(tz=UTC)

    logfire.force_flush(timeout_millis=10000)
    logfire.shutdown(timeout_millis=10000, flush=True)

    output_text = result.output if isinstance(result.output, str) else str(result.output)

    return {
        'question': question,
        'documents_count': len(documents),
        'started_at': started_at.isoformat(),
        'finished_at': finished_at.isoformat(),
        'answer_preview': output_text[:300],
        'window_start': (started_at - timedelta(minutes=2)).isoformat(),
        'window_end': (finished_at + timedelta(minutes=2)).isoformat(),
    }


def main():
    result = run_agent()
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
