import PyPDF2
import os  # Import os for potential future use or debugging


def process_pdf(file_stream):  # Renamed to process_pdf to match endpoints.py
    print(f"DEBUG: Entering process_pdf function.")
    text = ""
    try:
        reader = PyPDF2.PdfReader(file_stream)
        num_pages = len(reader.pages)
        print(f"DEBUG: PDF opened successfully. Number of pages: {num_pages}.")
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        print(f"DEBUG: Text extracted from PDF. Total text length: {len(text)}.")
        return text
    except Exception as e:
        print(f"ERROR: Error extracting text from PDF: {e}")
        return ""


def split_text_into_chunks(text, chunk_size=1000, overlap=100):
    print(f"DEBUG: Entering split_text_into_chunks. Text length: {len(text)}")
    chunks = []
    if not text:
        print("DEBUG: No text to split into chunks.")
        return chunks

    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
        if start >= len(text) - overlap and start < len(text):
            break
        elif start >= len(text):
            break
    print(f"DEBUG: Split into {len(chunks)} chunks.")
    return chunks