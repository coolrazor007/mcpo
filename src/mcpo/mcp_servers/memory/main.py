import argparse
from pydantic import EmailStr
from datetime import datetime
import os
import sys
import requests
import numpy as np
import weaviate
from weaviate.classes.init import AdditionalConfig, Timeout
from weaviate.classes.config import Property, DataType, Configure

# --- Existing functions: get_weaviate_client, collection_exists, create_collection_handler, etc. ---

def get_weaviate_client():
    weaviate_host = os.environ.get("WEAVIATE_HOST", "localhost")
    weaviate_port = int(os.environ.get("WEAVIATE_PORT", "8080"))
    return weaviate.connect_to_custom(
        http_host=weaviate_host,
        http_port=weaviate_port,
        http_secure=False,
        grpc_host=weaviate_host,
        grpc_port=50051,
        grpc_secure=False,
        skip_init_checks=True,
        additional_config=AdditionalConfig(
            timeout=Timeout(init=30, query=120, insert=120)
        )
    )

def collection_exists(client_weaviate, collection_name):
    return client_weaviate.collections.exists(collection_name)

def create_collection_handler(collection_name: str, properties: dict, vectorizer_config=None):
    properties_list = []
    for prop_name, prop_type in properties.items():
        data_type = DataType[prop_type.upper()]
        properties_list.append(Property(name=prop_name, data_type=data_type))
    if collection_exists(client_weaviate, collection_name):
        return
    client_weaviate.collections.create(
        name=collection_name,
        properties=properties_list,
        vectorizer_config=vectorizer_config
    )

def get_ollama_embedding(text: str):
    embedding_url = os.environ.get("OLLAMA_EMBEDDING_URL", "http://host.docker.internal:11434/api/embeddings")
    embedding_model = os.environ.get("EMBEDDING_MODEL", "nomic-embed-text")
    resp = requests.post(embedding_url, json={"model": embedding_model, "input": text})
    resp.raise_for_status()
    data = resp.json()
    if "embedding" in data:
        return data["embedding"]
    elif "embeddings" in data:
        return data["embeddings"][0]
    else:
        raise ValueError("No embedding returned from Ollama.")

def save_core_memory(user_email, core_memory, timestamp):
    client_weaviate = get_weaviate_client()
    sanitized_email = user_email.replace('@', '_').replace('.', '_')
    collection_name = f"{sanitized_email}_core_memories"
    collection_name = collection_name[0].upper() + collection_name[1:]
    if not collection_exists(client_weaviate, collection_name):
        create_collection_handler(
            collection_name,
            {"timestamp": "text", "core_memory": "text"},
            vectorizer_config=Configure.Vectorizer.none()
        )
    core_memory_vector = get_ollama_embedding(core_memory)
    core_memory_vector = np.array(core_memory_vector, dtype=np.float32).flatten().tolist()
    if not all(isinstance(v, float) for v in core_memory_vector):
        raise ValueError("Embedding vector contains invalid values. Ensure it's a flat list of floats.")
    weaviate_payload = {"timestamp": timestamp, "core_memory": core_memory}
    collection = client_weaviate.collections.get(collection_name)
    collection.data.insert(properties=weaviate_payload, vector=core_memory_vector)
    return "Successfully added the core memory to Weaviate"

# FastAPI app and endpoint remain below


# --- CLI entry point ---
def main():
    parser = argparse.ArgumentParser(description="MCP Memory Tool CLI")
    parser.add_argument("--user_email", required=True, type=str)
    parser.add_argument("--core_memory", required=True, type=str)
    parser.add_argument("--timestamp", required=True, type=str)
    args = parser.parse_args()

    # Optionally validate email
    try:
        email = EmailStr(args.user_email)
    except Exception as e:
        print({"status": "error", "detail": f"Invalid email: {e}"})
        sys.exit(1)

    try:
        result = save_core_memory(args.user_email, args.core_memory, args.timestamp)
        print({"status": "success", "detail": result})
        sys.exit(0)
    except Exception as e:
        print({"status": "error", "detail": str(e)})
        sys.exit(1)

if __name__ == "__main__":
    main()
