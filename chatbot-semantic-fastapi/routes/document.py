import os
import openai
from datetime import datetime

from fastapi import APIRouter, UploadFile
from dotenv import load_dotenv
from models.document import DocumentInputRequest, DocumentInputResponse, DocumentRetrieveRequest,DocumentResponse, DocumentRetrieveResponse
from utils.chunking_utils import prep_documents_for_vector_storage
from utils import embed

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
document_router = APIRouter()

@document_router.post("/ingest", response_model=DocumentInputResponse)
async def document_ingest(document: UploadFile): #request: DocumentInputRequest
    # chunking_strategy = request.chunking_strategy

    # if chunking_strategy == "sentence":
    #     chunks = re.split(r' *[\.\?!][\'"\)\]]* *', text)
    # elif chunking_strategy == "paragraph":
    #     chunks = text.split('\n')
    # elif chunking_strategy == "none":
    #     chunks = [text]
    # elif 'overlapping' in chunking_strategy:
    #     _, max_tokens, overlapping_factor = chunking_strategy.split('-')
    #     chunks = overlapping_chunks(text, max_tokens=500, overlapping_factor=5)
    # else:
    #     raise Exception("Invalid chunking strategy")
    print("sending to vector index")
    ids, texts, metadatas = prep_documents_for_vector_storage(document)
    embedding_engine = embed.get_embedding_engine()
    vector_index = embed.create_vector_index(
        embed.INDEX_NAME, embedding_engine, texts, metadatas)

    return DocumentInputResponse(chunks_count=vector_index._collection.count())

@document_router.post("/retrieve", response_model=list[DocumentResponse])
async def document_retrieve(request: DocumentRetrieveRequest):
    query = request.query
    num_results = request.num_results
    embedding_engine = embed.get_embedding_engine(allowed_special="all")

    print("connecting to vector storage")
    vector_index = embed.connect_to_vector_index(
        embed.INDEX_NAME, embedding_engine
    )
    print("connected to vector storage")

    sources_and_scores = vector_index.similarity_search_with_relevance_scores(query, k=num_results)
    results = [
        DocumentResponse(
            text=r[0].page_content,
            date_uploaded=1,
            score=r[1],
            id=r[0].metadata['page']
        ) for r in sources_and_scores
    ]

    return results