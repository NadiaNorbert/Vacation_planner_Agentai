from openai import OpenAI
from qdrant_client import QdrantClient
from c1.retri import retrieve_chunks

qdrant_client = QdrantClient(
    url="your_url", 
    api_key="your_apikey",
)

openai_client = OpenAI(base_url="your_url", api_key="your_apikey")

COLLECTION_NAME = "document_chunks_3"

def create_collection_if_not_exists():
    """Create a collection if it doesn't exist"""
    collections = qdrant_client.get_collections().collections
    collection_names = [collection.name for collection in collections]
    
    if COLLECTION_NAME not in collection_names:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,

        )
        print(f"Collection '{COLLECTION_NAME}' created.")
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")

def get_embedding(text):
    """Get embedding for a text using SentenceTransformer"""
    from sentence_transformers import SentenceTransformer
    
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    # If text is a single string, wrap it in a list
    if isinstance(text, str):
        embedding_vector = model.encode([text])[0]
    else:
        embedding_vector = model.encode(text)[0]
    
    return embedding_vector


def retrieve_chunks(query, limit=5):
    """Retrieve relevant document chunks based on a query"""
    query_embedding = get_embedding(query)
    
    search_result = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=limit
    )
    
    results = []
    for result in search_result:
        results.append({
            "text": result.payload["text"],
            "score": result.score,
            "chunk_index": result.payload["chunk_index"],
            "document_id": result.payload["document_id"]
        })
    
    return results

def chat(question: str):
    output = retrieve_chunks(question)

    prompt = f"""
        question: {question}
        output: {output[0]['text']}
        answer the question based on the output
    """

    #print(prompt)

    stream = qdrant_client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
            {
                "role": "user",
                "content": prompt,
            },
            {
                "role": "system",
                "content": """You are a helpful assistant that can answer questions about the world. your name is zara """,
            },
        ],
        stream=True,
    )

    for chunk in stream:
        # print(chunk)
        print(chunk.choices[0].delta.content, end="", flush=True)

