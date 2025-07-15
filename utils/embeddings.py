import requests
import json
from app.config import Config

def generate_embedding(text: str) -> list:
    ollama_host = Config.OLLAMA_HOST
    url = f"{ollama_host}/api/embeddings"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": Config.OLLAMA_EMBEDDING_MODEL_NAME,
        "prompt": text
    }

    print(f"🛰️ Connecting to Ollama at {url}")
    print(f"📤 Payload length: {len(text)} characters")

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"📡 Status code: {response.status_code}")
        print(f"📥 Response body: {response.text}")

        response.raise_for_status()
        result = response.json()

        if "embedding" not in result:
            raise ValueError(f"⚠️ 'embedding' key not found in Ollama response: {result}")

        if not result["embedding"]:
            raise ValueError("⚠️ Ollama returned an empty embedding list.")

        print("✅ Embedding generated successfully.")
        return result["embedding"]

    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP error while calling Ollama: {e}")
        return []

    except ValueError as ve:
        print(f"⚠️ Data error: {ve}")
        return []
