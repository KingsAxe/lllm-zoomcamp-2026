# Homework 4: Evaluation

This Week 4 workspace evaluates retrieval quality for the LLM Zoomcamp 2026 materials using the pinned course commit `8c1834d`.

## Objective

The homework measures how well text search, vector search, and hybrid search recover the correct lesson page for ground-truth questions. It also measures the prompt-token usage of Qwen-based structured question generation for the first three Week 1 lesson pages.

## Reused Infrastructure

- Week 2 ONNX embedder implementation
- Week 2 local `Xenova/all-MiniLM-L6-v2` model files
- `GithubRepositoryDataReader`
- `chunk_documents`
- `minsearch.Index`
- `minsearch.VectorSearch`

No second embedding model is downloaded in this folder. The notebook resolves the existing Week 2 model path relative to the repository root.

## Setup

```powershell
cd homework_04_evaluation
uv sync
```

Create a local `.env` only if needed. The notebook can use:

- `QWEN_API_KEY`
- `QWEN_BASE_URL`
- `QWEN_MODEL`

If `QWEN_BASE_URL` or `QWEN_MODEL` are not set locally, the helper code falls back to the verified DashScope-compatible Qwen endpoint and `qwen-plus`. Do not commit secrets.

## Run

```powershell
.\.venv\Scripts\jupyter-notebook.exe homework_04_evaluation.ipynb
```

The notebook is organized into:

1. Setup
2. Data loading
3. Ground-truth question generation
4. Index construction
5. Text-search result
6. Vector-search result
7. Evaluation metrics
8. Text evaluation
9. Vector evaluation
10. Hybrid tuning
11. Final answers

## Dependencies

The Week 4 environment includes:

- `gitsource`
- `jupyter`
- `minsearch`
- `numpy`
- `onnxruntime`
- `openai`
- `pandas`
- `pydantic`
- `python-dotenv`
- `tokenizers`

The ONNX model is reused from Week 2 and is not committed from this folder.
The official `ground-truth.csv` is stored in this folder and used directly by the notebook.
