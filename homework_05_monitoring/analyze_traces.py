from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


def main():
    db_path = Path('traces.db')
    if not db_path.exists():
        raise FileNotFoundError('traces.db does not exist yet.')

    with sqlite3.connect(db_path) as conn:
        spans = pd.read_sql_query('SELECT * FROM spans ORDER BY start_time', conn)

    print('Span names:', sorted(spans['name'].unique().tolist()))
    print('Counts by span:')
    print(spans['name'].value_counts())
    print('Duration totals excluding rag:')
    print(spans[spans['name'] != 'rag'].groupby('name')['duration_ms'].sum().sort_values(ascending=False))
    print('LLM input tokens:', spans[spans['name'] == 'llm']['input_tokens'].astype(int).tolist())


if __name__ == '__main__':
    main()
