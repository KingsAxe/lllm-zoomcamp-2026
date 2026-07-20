from __future__ import annotations

import requests
from minsearch import Index

DOCS_URL = 'https://datatalks.club/faq/json/courses.json'
URL_PREFIX = 'https://datatalks.club/faq'


def load_faq_data() -> list[dict]:
    response = requests.get(DOCS_URL, timeout=30)
    response.raise_for_status()
    courses_raw = response.json()

    documents: list[dict] = []
    for course in courses_raw:
        course_url = f"{URL_PREFIX}{course['path']}"
        course_response = requests.get(course_url, timeout=30)
        course_response.raise_for_status()
        course_data = course_response.json()
        documents.extend(course_data)

    return documents


def build_index(documents: list[dict]) -> Index:
    index = Index(
        text_fields=['question', 'section', 'answer'],
        keyword_fields=['course'],
    )
    index.fit(documents)
    return index
