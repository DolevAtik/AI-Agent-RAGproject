from typing import List

def create_rag_prompt(question: str, context: List[str]) -> str:
    context_str = "\n".join([f"Document excerpt: {c}" for c in context]) #
    prompt = f"""
    Based on the following information from the documents:
    {context_str}

    Answer the following question accurately, concisely, and by citing the relevant sources (document excerpts).
    If the answer is not available in the provided context, state that clearly.
    User question: {question}

    Answer:
    """
    return prompt