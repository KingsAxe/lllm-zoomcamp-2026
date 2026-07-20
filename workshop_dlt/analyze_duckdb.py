from __future__ import annotations

import duckdb

DUCKDB_PATH = 'workshop_logfire.duckdb'
TRACE_ID = '019f8080cd4c27a64caf5b4a812a5671'


def summarize_duckdb(db_path: str = DUCKDB_PATH, trace_id: str = TRACE_ID) -> dict:
    con = duckdb.connect(db_path, read_only=True)

    table_rows = con.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'agent_traces' ORDER BY table_name"
    ).fetchall()
    table_names = [row[0] for row in table_rows]

    trace_rows = con.execute(
        f"""
        SELECT trace_id, span_name, parent_span_id, duration,
               attributes__gen_ai_usage_input_tokens,
               attributes__gen_ai_aggregated_usage_input_tokens,
               attributes__gen_ai_usage_output_tokens,
               attributes__gen_ai_aggregated_usage_output_tokens,
               attributes__gen_ai_tool_name
        FROM agent_traces.records
        WHERE trace_id = '{trace_id}'
        ORDER BY start_timestamp
        """
    ).fetchall()

    llm_input_tokens = [row[4] for row in trace_rows if row[1] == 'chat qwen-plus' and row[4] is not None]
    total_input_tokens = sum(llm_input_tokens)

    return {
        'table_count': len(table_names),
        'table_names': table_names,
        'trace_rows': trace_rows,
        'llm_input_tokens': llm_input_tokens,
        'total_input_tokens': total_input_tokens,
    }


if __name__ == '__main__':
    summary = summarize_duckdb()
    print('table_count', summary['table_count'])
    print('table_names', summary['table_names'])
    print('trace_rows')
    for row in summary['trace_rows']:
        print(row)
    print('llm_input_tokens', summary['llm_input_tokens'])
    print('total_input_tokens', summary['total_input_tokens'])
