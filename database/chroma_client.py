import chromadb
from app.config import Config

class ChromaDBClient:
    def __init__(self):
        self.client = chromadb.HttpClient(host=Config.CHROMADB_HOST, port=Config.CHROMADB_PORT)
        self.collection = self.client.get_or_create_collection(name="research_papers")

    def add_document(self, ids: list, embeddings: list, metadatas: list, documents: list):
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )

    def query_documents(self, query_embedding: list, n_results: int = 5):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )