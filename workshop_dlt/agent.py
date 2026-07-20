from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from minsearch import Index
from openai import OpenAI
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

INSTRUCTIONS = """
You're a course teaching assistant. You're given a question from a course student and your task is to answer it.
You must call the search function at least once before you answer any user question.
If you want to look up information, use the search function. Use as many keywords from the user question as possible when making first requests.
Make multiple searches. First perform search, analyze the results and then perform more searches.
The question has to be about the course or its logistics, offtopic questions shouldn't be answered.
If the search returns nothing, it's likely an off-topic question.
If you can't answer the question using FAQ, don't do it yourself. Only use the facts from the FAQ database.
At the end, ask if there are other areas that the user wants to explore.
""".strip()

DEFAULT_QWEN_BASE_URL = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1'
DEFAULT_QWEN_MODEL = 'qwen-plus'
DEFAULT_LOGFIRE_BASE_URL = 'https://logfire-us.pydantic.dev'
FINAL_QUERY = 'How do I run Ollama locally?'


@dataclass
class SearchDeps:
    index: Index


def load_env() -> dict[str, str | None]:
    env_paths = [
        Path(__file__).resolve().parent / '.env',
        Path(__file__).resolve().parents[1] / '.env',
    ]
    for path in env_paths:
        if path.exists():
            load_dotenv(path, override=False)

    return {
        'qwen_api_key': os.getenv('QWEN_API_KEY'),
        'qwen_base_url': os.getenv('QWEN_BASE_URL') or DEFAULT_QWEN_BASE_URL,
        'qwen_model': os.getenv('QWEN_MODEL') or DEFAULT_QWEN_MODEL,
        'logfire_token': os.getenv('LOGFIRE_TOKEN'),
        'logfire_read_token': os.getenv('LOGFIRE_READ_TOKEN'),
        'logfire_base_url': os.getenv('LOGFIRE_BASE_URL') or DEFAULT_LOGFIRE_BASE_URL,
    }


def create_model_and_client():
    cfg = load_env()
    if not cfg['qwen_api_key']:
        raise RuntimeError('QWEN_API_KEY is not available in the environment.')

    provider = OpenAIProvider(base_url=cfg['qwen_base_url'], api_key=cfg['qwen_api_key'])
    model = OpenAIChatModel(cfg['qwen_model'], provider=provider)
    client = OpenAI(api_key=cfg['qwen_api_key'], base_url=cfg['qwen_base_url'])
    return model, client, cfg


faq_agent: Agent[SearchDeps, str] | None = None


def get_agent() -> Agent[SearchDeps, str]:
    global faq_agent
    if faq_agent is not None:
        return faq_agent

    model, _, _ = create_model_and_client()
    faq_agent = Agent(
        model,
        deps_type=SearchDeps,
        instructions=INSTRUCTIONS,
        output_type=str,
    )

    @faq_agent.tool
    def search(ctx: RunContext[SearchDeps], query: str) -> list[dict]:
        """Search the FAQ database for entries matching the given query."""
        boost_dict = {'question': 3.0, 'section': 0.5}
        filter_dict = {'course': 'llm-zoomcamp'}
        results = ctx.deps.index.search(
            query,
            num_results=5,
            boost_dict=boost_dict,
            filter_dict=filter_dict,
        )
        return results

    return faq_agent
