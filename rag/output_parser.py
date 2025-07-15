from app.models import AnswerResponse, SourceCitation
from typing import List, Dict

def parse_llm_output(llm_raw_output: str, retrieved_citations: List[Dict]) -> AnswerResponse:
    answer_text = llm_raw_output

    parsed_citations = [SourceCitation(document_name=c['document_name'], chunk_id=c['chunk_id']) for c in retrieved_citations]

    return AnswerResponse(
        answer=answer_text,
        citations=parsed_citations,
        confidence_score=None
    )