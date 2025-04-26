from pinecone import Pinecone
import os

# Initialize Pinecone client and create an index with integrated inference
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Create a dense index using Llama integrated embedding if it doesn't exist
INDEX_NAME = "zomato-rag"
try:
    pc.create_index_for_model(
        name=INDEX_NAME,
        cloud="aws",
        region="us-east-1",
        embed={
            "model": "llama-text-embed-v2",
            "field_map": {"text": "text"}
        }
    )
except Exception:
    # Index may already exist
    pass

# Connect to the index
index = pc.Index(INDEX_NAME)

async def upsert_data(
    id: str,
    text: str,
    namespace: str = None
) -> None:
    """Upsert a text record into Pinecone using integrated embeddings."""
    record = {
        "id": id,                     # e.g., MongoDB Restaurant or Menu item ID
        "text": text                  # raw text to embed
    }
    try:
        index.upsert_records(
            namespace=namespace,
            records=[record]
        )
    except Exception as e:
        # Handle or re-raise exception as needed
        raise e

async def fetch_data(
    query_text: str,
    top_k: int = 3,
    namespace: str = None
) -> list:
    """Perform similarity search over text records using integrated embeddings."""
    query_payload = {
        "inputs": {"text": query_text},
        "top_k": top_k
    }
    try:
        result = index.search(
            namespace=namespace,
            query=query_payload,
            include_metadata=True
        )
        return result.get("matches", [])
    except Exception as e:
        # Handle or re-raise exception as needed
        raise e
