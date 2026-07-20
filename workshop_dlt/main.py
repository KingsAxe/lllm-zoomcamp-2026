from __future__ import annotations

from agent import FINAL_QUERY, SearchDeps, get_agent
from ingest import build_index, load_faq_data


def build_agent_and_deps():
    documents = load_faq_data()
    index = build_index(documents)
    deps = SearchDeps(index=index)
    agent = get_agent()
    return agent, deps, documents


def run_query(question: str = FINAL_QUERY):
    agent, deps, documents = build_agent_and_deps()
    result = agent.run_sync(question, deps=deps)
    return {
        'question': question,
        'documents_count': len(documents),
        'answer': result.output,
        'messages': result.all_messages_json().decode() if hasattr(result, 'all_messages_json') else None,
    }


def main():
    result = run_query()
    print('Documents:', result['documents_count'])
    print('Question:', result['question'])
    print('Answer preview:', result['answer'][:500])


if __name__ == '__main__':
    main()
