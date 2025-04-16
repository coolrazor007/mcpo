from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
import os
import sys

import requests
import numpy as np
import weaviate
from weaviate.classes.init import AdditionalConfig, Timeout
from weaviate.classes.config import Property, DataType, Configure
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
import os

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


app = FastAPI()

# Dummy authentication dependency (replace with real auth in prod)
def authenticate_user(user_email: str):
    # In production, validate user session/token and return user info
    class User:
        def __init__(self, email):
            self.email = email
    return User(user_email)

class SaveCoreMemoryRequest(BaseModel):
    user_email: EmailStr
    core_memory: str
    timestamp: str  # ISO 8601

@app.post("/memory/save_core_memory")
def save_core_memory_endpoint(
    req: SaveCoreMemoryRequest,
    user=Depends(lambda: authenticate_user(req.user_email))
):
    if user.email != req.user_email:
        raise HTTPException(status_code=403, detail="Unauthorized")
    try:
        result = save_core_memory(
            req.user_email,
            req.core_memory,
            req.timestamp
        )
        return {"status": "success", "detail": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
