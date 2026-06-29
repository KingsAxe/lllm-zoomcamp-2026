# Homework 2: Vector Search

This folder contains a self-contained solution for LLM Zoomcamp 2026 Homework 2 using the course ONNX embedder and the pinned course commit `8c1834d`.

## Included

- `homework_02_vector_search.ipynb`: executed homework notebook with visible outputs
- `embedder.py`: local ONNX embedder helper from the course materials
- `download.py`: course download helper retained for reference
- `pyproject.toml` and `uv.lock`: reproducible Week 2 environment

## Rerun From A Clean Clone

```powershell
cd homework_02_vector_search
$env:UV_CACHE_DIR=(Resolve-Path ..\.tmp).Path
uv sync
.\.venv\Scripts\python.exe -m ipykernel install --user --name homework-02-vector-search --display-name "homework-02-vector-search"
.\.venv\Scripts\jupyter-notebook.exe homework_02_vector_search.ipynb
```

If the local ONNX model is missing, run:

```powershell
.\.venv\Scripts\python.exe download.py
```

The `models/` and `.venv/` directories are intentionally ignored and should not be committed.
