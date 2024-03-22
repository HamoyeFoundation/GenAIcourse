from pydantic import BaseModel
from typing import List
from datetime import datetime

class DocumentInputRequest(BaseModel):
    text: str
    chunking_strategy: str = "paragraph"

class DocumentInputResponse(BaseModel):
    chunks_count: int

class DocumentRetrieveRequest(BaseModel):
    query: str
    num_results: int

class DocumentResponse(BaseModel):
    text: str
    date_uploaded: datetime
    score: float
    id: int

class DocumentRetrieveResponse(BaseModel):
    document: list[DocumentResponse]