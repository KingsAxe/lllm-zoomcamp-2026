from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from gitsource import GithubRepositoryDataReader, chunk_documents
from minsearch import Index, VectorSearch
from openai import OpenAI
from pydantic import BaseModel


COURSE_COMMIT = "8c1834d"
DEFAULT_QWEN_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
DEFAULT_QWEN_MODEL = "qwen-plus"
MODEL_DIR = Path(__file__).resolve().parents[1] / "homework_02_vector_search" / "models" / "Xenova" / "all-MiniLM-L6-v2"


class Questions(BaseModel):
    questions: list[str]


def load_qwen_client(env_paths: list[Path] | None = None) -> tuple[OpenAI, str]:
    if env_paths is None:
        env_paths = [
            Path(__file__).resolve().parent / ".env",
            Path(__file__).resolve().parents[1] / ".env",
        ]

    for path in env_paths:
        if path.exists():
            load_dotenv(path, override=False)

    api_key = os.getenv("QWEN_API_KEY")
    base_url = os.getenv("QWEN_BASE_URL") or DEFAULT_QWEN_BASE_URL
    model = os.getenv("QWEN_MODEL") or DEFAULT_QWEN_MODEL

    if not api_key:
        raise RuntimeError("QWEN_API_KEY is not available in the environment.")

    return OpenAI(api_key=api_key, base_url=base_url), model


def load_documents() -> list[dict]:
    reader = GithubRepositoryDataReader(
        repo_owner="DataTalksClub",
        repo_name="llm-zoomcamp",
        commit_id=COURSE_COMMIT,
        allowed_extensions={"md"},
        filename_filter=lambda path: "/lessons/" in path,
    )
    return [file.parse() for file in reader.read()]


def chunk_lesson_documents(documents: list[dict], size: int = 2000, step: int = 1000) -> list[dict]:
    return chunk_documents(documents, size=size, step=step)


def build_indexes(chunks: list[dict], embedder, batch_size: int = 32) -> tuple[np.ndarray, Index, VectorSearch]:
    matrices = []
    for start in range(0, len(chunks), batch_size):
        batch = [chunk["content"] for chunk in chunks[start:start + batch_size]]
        matrices.append(embedder.encode_batch(batch))

    vectors = np.vstack(matrices)

    text_index = Index(text_fields=["content"], keyword_fields=["filename"])
    text_index.fit(chunks)

    vector_index = VectorSearch(keyword_fields=["filename"], numeric_fields=["start"])
    vector_index.fit(vectors=vectors, payload=chunks)

    return vectors, text_index, vector_index


def text_search(text_index: Index, query: str, num_results: int = 5) -> list[dict]:
    return text_index.search(query, num_results=num_results)


def vector_search(vector_index: VectorSearch, embedder, query: str, num_results: int = 5) -> list[dict]:
    query_vector = embedder.encode(query)
    return vector_index.search(query_vector, num_results=num_results)


def rrf(result_lists: list[list[dict]], k: int = 60, num_results: int = 5) -> list[dict]:
    scores = {}
    docs = {}

    for results in result_lists:
        for rank, doc in enumerate(results):
            key = (doc["filename"], doc["start"])
            scores[key] = scores.get(key, 0.0) + 1 / (k + rank)
            docs[key] = doc

    ranked = sorted(scores, key=scores.get, reverse=True)
    return [docs[key] for key in ranked[:num_results]]


def hybrid_search(text_index: Index, vector_index: VectorSearch, embedder, query: str, k: int = 60, num_results: int = 5) -> list[dict]:
    text_results = text_search(text_index, query, num_results=10)
    vector_results = vector_search(vector_index, embedder, query, num_results=10)
    return rrf([text_results, vector_results], k=k, num_results=num_results)


def llm_structured(client: OpenAI, model: str, prompt: str, response_model: type[BaseModel]):
    try:
        response = client.beta.chat.completions.parse(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format=response_model,
        )
        parsed = response.choices[0].message.parsed
        usage = response.usage
    except Exception:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Return valid JSON only."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        parsed = response_model.model_validate(json.loads(content))
        usage = response.usage

    return {"parsed": parsed, "usage": usage}
