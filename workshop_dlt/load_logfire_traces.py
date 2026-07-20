from __future__ import annotations

from datetime import datetime
from pathlib import Path

import dlt
from logfire.query_client import LogfireQueryClient

from agent import FINAL_QUERY, load_env

FINAL_RUN = {
    'question': FINAL_QUERY,
    'trace_id': '019f8080cd4c27a64caf5b4a812a5671',
    'window_start': '2026-07-20T17:06:53.297268+00:00',
    'window_end': '2026-07-20T17:11:30.707454+00:00',
}
DUCKDB_PATH = 'workshop_logfire.duckdb'


def fetch_records() -> list[dict]:
    cfg = load_env()
    client = LogfireQueryClient(read_token=cfg['logfire_read_token'], base_url=cfg['logfire_base_url'])
    result = client.query_json_rows(
        sql='select * from records order by start_timestamp asc',
        min_timestamp=datetime.fromisoformat(FINAL_RUN['window_start']),
        max_timestamp=datetime.fromisoformat(FINAL_RUN['window_end']),
        limit=100,
    )
    return [row for row in result['rows'] if row.get('trace_id') == FINAL_RUN['trace_id']]


@dlt.resource(name='records', write_disposition='replace')
def records_resource():
    yield from fetch_records()


def load_to_duckdb(db_path: str = DUCKDB_PATH):
    pipeline = dlt.pipeline(
        pipeline_name='workshop_dlt_pipeline',
        destination='duckdb',
        dataset_name='agent_traces',
        progress='log',
    )
    destination = dlt.destinations.duckdb(credentials=db_path)
    load_info = pipeline.run(records_resource(), destination=destination)
    return load_info


if __name__ == '__main__':
    info = load_to_duckdb()
    print(info)
