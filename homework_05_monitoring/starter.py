from __future__ import annotations

from rag_helper import QUERY, QwenChatAdapter, RAGBase, build_index, load_documents, load_qwen_client


def main():
    client, model = load_qwen_client()
    documents = load_documents()
    assert len(documents) == 72, len(documents)
    index = build_index(documents)
    rag = RAGBase(index=index, llm_client=QwenChatAdapter(client, model))
    result = rag.rag(QUERY)
    print("Answer preview:")
    print(result["answer"][:500])
    print("Input tokens:", result["input_tokens"])
    print("Output tokens:", result["output_tokens"])


if __name__ == "__main__":
    main()
