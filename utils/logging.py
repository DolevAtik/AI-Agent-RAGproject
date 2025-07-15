from database.mongo_client import MongoDBClient
from datetime import datetime

def log_interaction(query: str, retrieved_chunks: list, generated_answer: str, source_citations: list, processing_metadata: dict):
    mongo_client = MongoDBClient()
    log_entry = {
        "timestamp": datetime.now(),
        "user_query": query,
        "retrieved_document_chunks": retrieved_chunks,
        "generated_answer": generated_answer,
        "source_citations": source_citations,
        "processing_metadata": processing_metadata
    }
    mongo_client.logs_collection.insert_one(log_entry)