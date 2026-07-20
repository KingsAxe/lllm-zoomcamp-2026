from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from gitsource import GithubRepositoryDataReader
from minsearch import Index
from openai import OpenAI


COURSE_COMMIT = "8c1834d"
DEFAULT_QWEN_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
DEFAULT_QWEN_MODEL = "qwen-plus"
QUERY = "How does the agentic loop keep calling the model until it stops?"
INPUT_COST_PER_1K = 0.0004
OUTPUT_COST_PER_1K = 0.0012


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


def build_index(documents: list[dict]) -> Index:
    index = Index(text_fields=["content"], keyword_fields=["filename"])
    index.fit(documents)
    return index


class QwenChatAdapter:
    def __init__(self, client: OpenAI, model: str):
        self.client = client
        self.model = model
        self.provider = "qwen"

    def complete(self, prompt: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You answer questions about the LLM Zoomcamp course using only the provided context.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        message = response.choices[0].message.content or ""
        usage = response.usage
        input_tokens = getattr(usage, "prompt_tokens", None) or 0
        output_tokens = getattr(usage, "completion_tokens", None) or 0
        cost = (input_tokens / 1000) * INPUT_COST_PER_1K + (output_tokens / 1000) * OUTPUT_COST_PER_1K
        return {
            "text": message,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost,
            "model": self.model,
            "provider": self.provider,
        }


class RAGBase:
    def __init__(self, index: Index, llm_client: QwenChatAdapter):
        self.index = index
        self.llm_client = llm_client

    def search(self, query: str, num_results: int = 5) -> list[dict]:
        return self.index.search(query, num_results=num_results)

    def build_context(self, search_results: list[dict]) -> str:
        parts = []
        for doc in search_results:
            parts.append(f"Filename: {doc['filename']}\nContent:\n{doc['content']}")
        return "\n\n---\n\n".join(parts)

    def build_prompt(self, query: str, search_results: list[dict]) -> str:
        context = self.build_context(search_results)
        return (
            "Answer the user question using only the provided course context.\n"
            "If the answer is not in the context, say so.\n\n"
            f"Question:\n{query}\n\n"
            f"Context:\n{context}"
        )

    def llm(self, prompt: str) -> dict:
        return self.llm_client.complete(prompt)

    def rag(self, query: str) -> dict:
        results = self.search(query)
        prompt = self.build_prompt(query, results)
        answer = self.llm(prompt)
        return {
            "query": query,
            "search_results": results,
            "prompt": prompt,
            "answer": answer["text"],
            "input_tokens": answer["input_tokens"],
            "output_tokens": answer["output_tokens"],
            "cost": answer["cost"],
            "model": answer["model"],
            "provider": answer["provider"],
        }
