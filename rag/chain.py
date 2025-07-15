import requests
import json
from typing import  Dict


from utils.embeddings import generate_embedding
from database.chroma_client import ChromaDBClient
from rag.prompt_templates import create_rag_prompt
from app.config import Config


class RAGChain:
    def __init__(self):
        self.chroma_client = ChromaDBClient()
        self.ollama_host = Config.OLLAMA_HOST
        self.ollama_llm_model_name = Config.OLLAMA_LLM_MODEL_NAME

    def retrieve_and_generate(self, question: str) -> Dict:
        print("DEBUG: Starting retrieve_and_generate")

        query_embedding = generate_embedding(question)
        if not query_embedding:
            print("DEBUG: Failed to generate embedding for question")
            return {
                "answer": "Error generating embedding for the question.",
                "citations": []
            }

        print("DEBUG: Querying ChromaDB for relevant documents...")
        retrieved_results = self.chroma_client.query_documents(query_embedding)

        relevant_chunks_data = []
        context_texts = []
        citations = []

        if retrieved_results and retrieved_results['documents']:
            print(f"DEBUG: Retrieved {len(retrieved_results['documents'][0])} chunks")
            for i, doc_content in enumerate(retrieved_results['documents'][0]):
                metadata = retrieved_results['metadatas'][0][i]
                relevant_chunks_data.append({
                    "document_name": metadata.get("document_name"),
                    "chunk_id": metadata.get("chunk_id"),
                    "content": doc_content
                })
                context_texts.append(doc_content)
                citations.append({
                    "document_name": metadata.get("document_name"),
                    "chunk_id": metadata.get("chunk_id")
                })

        if not context_texts:
            print("DEBUG: No relevant chunks found")
            return {
                "answer": "No relevant information found in the uploaded documents.",
                "citations": []
            }

        print("DEBUG: Constructing prompt...")
        prompt = create_rag_prompt(question, context_texts)
        print(f"DEBUG: Prompt length: {len(prompt)}")

        url = f"{self.ollama_host}/api/generate"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": self.ollama_llm_model_name,
            "prompt": prompt,
            "stream": False
        }

        print(f"DEBUG: Sending prompt to Ollama at {url}")
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data), timeout=500)
            print(f"DEBUG: Ollama generate response status = {response.status_code}")
            print("DEBUG: Ollama generate response text:", response.text[:500])

            response.raise_for_status()
            generated_text = response.json().get("response", "")
            return {
                "answer": generated_text,
                "citations": citations,
                "retrieved_chunks": relevant_chunks_data
            }

        except requests.exceptions.RequestException as e:
            print(f"ERROR: Failed to call Ollama generate: {e}")
            return {
                "answer": f"Error communicating with the LLM model: {str(e)}",
                "citations": []
            }


def warmup_model():
    print("🔥 Warming up the Ollama model...")

    # שלב 1: ליצור embedding קצר כדי לוודא שהמודל טעון
    dummy_text = "Warmup embedding text"
    embedding = generate_embedding(dummy_text)
    if embedding:
        print("✅ Embedding warmup successful.")
    else:
        print("⚠️ Embedding warmup failed.")

    # שלב 2: לשאול שאלה פשוטה כדי לוודא שה-LLM זמין
    try:
        dummy_question = "What is 2 + 2?"
        print(f"🧠 Sending dummy question to LLM: {dummy_question}")
        result = rag_chain.retrieve_and_generate(dummy_question)
        print(f"✅ LLM warmup response: {result['answer']}")
    except Exception as e:
        print(f"❌ Error during LLM warmup: {e}")
