import os

class Config:
    MONGODB_HOST = os.getenv('MONGODB_HOST', 'localhost')
    MONGODB_PORT = int(os.getenv('MONGODB_PORT', 27017))
    MONGODB_DB = os.getenv('MONGODB_DB', 'rag_logs')

    CHROMADB_HOST = os.getenv('CHROMADB_HOST', 'localhost')
    CHROMADB_PORT = int(os.getenv('CHROMADB_PORT', 8000))

    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://ollama:11434')
    OLLAMA_LLM_MODEL_NAME = os.getenv('OLLAMA_LLM_MODEL_NAME', 'mistral')
    OLLAMA_EMBEDDING_MODEL_NAME = os.getenv('OLLAMA_EMBEDDING_MODEL_NAME', 'nomic-embed-text')
