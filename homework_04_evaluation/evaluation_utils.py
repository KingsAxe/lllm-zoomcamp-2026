from __future__ import annotations

from typing import Callable


def compute_relevance(search_function: Callable[[str, int], list], question: str, expected_filename: str, num_results: int = 5) -> list[int]:
    results = search_function(question, num_results=num_results)
    relevance = [1 if result["filename"] == expected_filename else 0 for result in results]
    return relevance


def hit_rate(relevance_total: list[list[int]]) -> float:
    return sum(1 if any(row) else 0 for row in relevance_total) / len(relevance_total)


def mrr(relevance_total: list[list[int]]) -> float:
    total = 0.0
    for row in relevance_total:
        for rank, value in enumerate(row, start=1):
            if value:
                total += 1 / rank
                break
    return total / len(relevance_total)


def evaluate(ground_truth: list[dict], search_function: Callable[[str, int], list], num_results: int = 5) -> dict:
    relevance_total = [
        compute_relevance(search_function, row["question"], row["filename"], num_results=num_results)
        for row in ground_truth
    ]
    return {
        "relevance_total": relevance_total,
        "hit_rate": hit_rate(relevance_total),
        "mrr": mrr(relevance_total),
        "total_questions": len(ground_truth),
        "questions_with_hit": sum(1 if any(row) else 0 for row in relevance_total),
    }
