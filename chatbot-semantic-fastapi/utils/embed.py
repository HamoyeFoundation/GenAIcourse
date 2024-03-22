from pathlib import Path
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.chroma import Chroma

INDEX_NAME = "llms-search-retrieval"
VECTOR_DIR = Path("vectors")

def create_vector_index(index_name, embedding_engine, documents, metadatas):
    """Creates a vector db that offers similarity search."""
    files = VECTOR_DIR.glob(f"{index_name}.*")
    if files:
        for file in files:
            file.unlink()
        print("existing index wiped")

    index = Chroma.from_texts(
        texts=documents, embedding=embedding_engine,metadatas=metadatas, collection_name=index_name, persist_directory=str(VECTOR_DIR)
    )

    return index

def connect_to_vector_index(index_name, embedding_engine):
    """Adds the texts and metadatas to the vector index."""
    index = Chroma(persist_directory=str(VECTOR_DIR), embedding_function=embedding_engine, collection_name=index_name)

    return index

def get_embedding_engine(model="sentence-transformers/multi-qa-mpnet-base-cos-v1", **kwargs):
    """Retrieves the embedding engine"""
    # embedding_engine = OpenAIEmbeddings(model=model)
    # model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    embedding_engine = HuggingFaceEmbeddings(
        model_name=model,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    return embedding_engine
    