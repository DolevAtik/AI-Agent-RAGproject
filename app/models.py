from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=500)

class SourceCitation(BaseModel):
    document_name: str
    chunk_id: str

class AnswerResponse(BaseModel):
    answer: str
    citations: List[SourceCitation]
    confidence_score: Optional[float] = None