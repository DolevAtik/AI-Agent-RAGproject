# AI RAG Agent 🧠 

An AI-powered Flask application using Retrieval-Augmented Generation (RAG) to answer questions based on uploaded PDF documents. It leverages **ChromaDB** for document indexing and **Ollama** (e.g., with `mistral`) as the language model for generating responses.

---

## 🧪 How It Works  :

1. Upload PDF files via the Swagger UI or API.
2. Each document is split into chunks, embedded using `nomic-embed-text`, and stored in ChromaDB.
3. When a question is asked, relevant chunks are retrieved from the vector store.
4. A prompt is constructed and sent to the LLM (e.g., `mistral`).
5. The model generates an answer with citations pointing to the source document chunks.

---

## 🚀 Getting Started : 
- run the scripts by the order :
```bash
docker-compose up 
```
```bash
docker exec -it ragproject-ollama-1 ollama pull nomic-embed-text
docker exec -it ragproject-ollama-1 ollama pull mistral
```
```bash
docker-compose up --build
```

### Once running , access the Link:

### 👉 [http://localhost:5000/swagger](http://localhost:5000/swagger)

---

## 🔍 Swagger instructions :

The Swagger interface allows you to easily interact with the API:

1. **Upload PDF files**  
   Use the `POST /api/papers` endpoint , press `Try it out` to upload one or more PDF files , and then execute. 


1. **Ask a Question**  
   Use the `POST /api/ask` endpoint ,  press `Try it out` to provide a question as JSON format , and then execute.

2. **View the Response**  
   You'll receive:
   - The generated answer from the LLM
   - Citations pointing to relevant chunks from uploaded documents
   - The actual chunks that were used



---

### 🛠️ Tech Stack

- 🐍 Python + Flask
- 📄 MongoDB + Mongo Express
- 📚 ChromaDB (vector store)
- 🧠 Ollama LLM (e.g., `mistral`)
- 🔤 Embedding Model: `nomic-embed-text`
- 🐳 Docker & Docker Compose
- 🔎 Swagger/OpenAPI for API docs

---

### ✅ Prerequisites

- Python 3.10+
- Docker & Docker Compose installed
- [Ollama](https://ollama.com) installed locally and running
---
## **Happy building! 🚀**


