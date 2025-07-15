from flask import Blueprint, request, jsonify, current_app  # Added current_app
from pydantic import ValidationError
from werkzeug.utils import secure_filename
import os
from io import BytesIO

from app.models import QueryRequest, AnswerResponse
from utils.pdf_processor import process_pdf, split_text_into_chunks  # Changed to process_pdf
from utils.embeddings import generate_embedding
from database.chroma_client import ChromaDBClient
from rag.chain import RAGChain
from rag.output_parser import parse_llm_output
from utils.logging import log_interaction

api_blueprint = Blueprint('api', __name__)

# Initialize clients at module level
try:
    chroma_client = ChromaDBClient()
    print("DEBUG: ChromaDBClient initialized successfully.")
except Exception as e:
    print(f"ERROR: Failed to initialize ChromaDBClient: {e}")
    # Consider raising an exception or handling this more robustly if the app cannot function without it

try:
    rag_chain = RAGChain()
    print("DEBUG: RAGChain initialized successfully.")
except Exception as e:
    print(f"ERROR: Failed to initialize RAGChain: {e}")
    # Similar consideration for RAGChain


@api_blueprint.route('/papers', methods=['POST'])
def upload_papers():
    print("DEBUG: POST /api/papers endpoint hit.")
    if 'files' not in request.files:
        print("DEBUG: No 'files' part in request.")
        return jsonify({"error": "No files part"}), 400

    files = request.files.getlist('files')
    if not files:
        print("DEBUG: No selected file.")
        return jsonify({"error": "No selected file"}), 400

    uploaded_document_ids = []
    # No need for UPLOAD_FOLDER or saving to disk if processing directly from stream
    # upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    # if not os.path.exists(upload_folder):
    #     os.makedirs(upload_folder)

    for file in files:
        if file.filename == '':
            print("DEBUG: Empty filename skipped.")
            continue

        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            print(f"DEBUG: Processing file: {filename}")

            try:
                # Read file into BytesIO to pass to pdf_processor
                file_stream = BytesIO(file.read())
                print(f"DEBUG: File '{filename}' read into BytesIO.")

                # 1. Extract text
                print(f"DEBUG: Calling process_pdf for {filename}.")
                text = process_pdf(file_stream)  # Use process_pdf

                if not text:
                    print(f"DEBUG: No text extracted from {filename}.")
                    return jsonify({"error": f"Failed to process {filename}: no content extracted"}), 500

                print(f"DEBUG: Text extracted from {filename}. Length: {len(text)}.")

                # 2. Split into chunks
                chunks = split_text_into_chunks(text)

                if not chunks:
                    print(f"DEBUG: No chunks generated from {filename}.")
                    return jsonify({"error": f"Failed to process {filename}: no chunks generated"}), 500

                print(f"DEBUG: Text split into {len(chunks)} chunks for {filename}.")

                # 3. Generate embeddings and store
                chunk_ids = []
                chunk_embeddings = []
                chunk_metadatas = []

                for i, chunk in enumerate(chunks):
                    print(f"DEBUG: Generating embedding for chunk {i + 1} of {filename}.")
                    embedding = generate_embedding(chunk)
                    if embedding:
                        chunk_ids.append(f"{filename}_chunk_{i}")
                        chunk_embeddings.append(embedding)
                        chunk_metadatas.append({"document_name": filename, "chunk_id": f"chunk_{i}"})
                    else:
                        print(f"DEBUG: Embedding generation failed for chunk {i + 1} of {filename}.")

                if chunk_ids:
                    print(f"DEBUG: Adding {len(chunk_ids)} embeddings to ChromaDB for {filename}.")
                    chroma_client.add_document(
                        ids=chunk_ids,
                        embeddings=chunk_embeddings,
                        metadatas=chunk_metadatas,
                        documents=chunks
                    )
                    uploaded_document_ids.append(filename)
                    print(f"DEBUG: Document {filename} successfully processed and added to ChromaDB.")
                else:
                    print(f"DEBUG: No embeddings generated for {filename}.")
                    return jsonify({"error": f"Failed to process {filename}: no embeddings generated"}), 500

            except Exception as e:
                print(f"ERROR: Exception during PDF processing of {filename}: {e}")
                return jsonify({"error": f"Failed to process {filename}: {str(e)}"}), 500
        else:
            print(f"DEBUG: Invalid file type for {file.filename}.")
            return jsonify({"error": "Invalid file type. Only PDF files are allowed."}), 400

    if uploaded_document_ids:
        print(f"DEBUG: Successfully processed {len(uploaded_document_ids)} documents.")
        return jsonify({"status": "success", "uploaded_documents": uploaded_document_ids}), 200
    else:
        print("DEBUG: No PDFs were successfully processed.")
        return jsonify({"status": "failure", "message": "No PDFs were successfully processed."}), 400



@api_blueprint.route('/query', methods=['POST'])
def query_papers():
    print("DEBUG: POST /api/query endpoint hit.")

    # הדפסת נתוני הבקשה
    print("DEBUG: Raw request data:", request.data)
    print("DEBUG: request.json:", request.json)

    try:
        data = request.get_json(force=True)
        print("DEBUG: Parsed JSON:", data)
        query_data = QueryRequest(**data)
    except Exception as e:
        print(f"DEBUG: Failed to parse JSON: {e}")
        return jsonify({"error": "Failed to parse JSON", "details": str(e)}), 400

    question = query_data.question
    print(f"DEBUG: Received query: {question}")

    # עטיפת הקריאה ל־RAGChain
    try:
        print("DEBUG: Calling rag_chain.retrieve_and_generate...")
        rag_result = rag_chain.retrieve_and_generate(question)
        print("DEBUG: RAGChain response received.")
    except Exception as e:
        print(f"ERROR: RAGChain failed: {e}")
        return jsonify({"error": "RAG processing failed", "details": str(e)}), 500

    # המשך עיבוד התשובה
    generated_answer_text = rag_result.get("answer", "An error occurred or no answer could be generated.")
    retrieved_citations_data = rag_result.get("citations", [])
    retrieved_chunks_for_log = rag_result.get("retrieved_chunks", [])

    answer_response = parse_llm_output(generated_answer_text, retrieved_citations_data)

    log_interaction(
        query=question,
        retrieved_chunks=retrieved_chunks_for_log,
        generated_answer=answer_response.answer,
        source_citations=[c.dict() for c in answer_response.citations],
        processing_metadata={"status": "completed"}
    )
    print(f"DEBUG: Query processed. Answer length: {len(answer_response.answer)}.")
    return jsonify(answer_response.dict()), 200


