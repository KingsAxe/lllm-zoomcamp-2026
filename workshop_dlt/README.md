# dlt Workshop Homework

This workspace runs the Pydantic AI FAQ agent with Logfire instrumentation, loads the resulting trace records into DuckDB with dlt, and answers the three workshop homework questions.

## Objective

- Build the FAQ teaching-assistant agent with Pydantic AI
- Instrument the run with Logfire
- Pull Logfire `records` into DuckDB with dlt
- Analyze the trace for span count, table count, and input-token totals

## Setup

```powershell
cd workshop_dlt
uv sync
```

Required environment variables:

- `QWEN_API_KEY`
- `QWEN_BASE_URL`
- `QWEN_MODEL`
- `LOGFIRE_TOKEN`
- `LOGFIRE_READ_TOKEN`
- `LOGFIRE_BASE_URL`

## Run

```powershell
.\.venv\Scripts\python.exe run_logfire_agent.py
.\.venv\Scripts\python.exe load_logfire_traces.py
.\.venv\Scripts\python.exe analyze_duckdb.py
.\.venv\Scripts\jupyter-notebook.exe dlt_workshop.ipynb
```

## Notes

- `.env`, `.dlt/`, DuckDB files, and caches are ignored.
- No Docker is required.
- The final public notebook path is `workshop_dlt/dlt_workshop.ipynb`.
