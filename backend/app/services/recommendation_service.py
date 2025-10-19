import pinecone
import requests

# --- ⚙️ CONFIGURATION (with your hardcoded keys) ---
# Your keys are intentionally left in this file as requested.
PINECONE_API_KEY = "pcsk_3spAud_D66kNnQiYH4TF99hStEuThoSqjoingbaw7zXLRzRfPmvaXjurbpVMg38bdxU2gM"
INDEX_HOST = "https://recomend-6c7pmst.svc.aped-4627-b74a.pinecone.io"
HUGGING_FACE_TOKEN = "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"


API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}


models = {}

def startup_event():
    print("Connecting to Pinecone...")
    try:
        pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
        models['pinecone_index'] = pc.Index(host=INDEX_HOST)
        print("✅ Pinecone connected successfully.")
    except Exception as e:
        print(f"❌ FATAL: Could not initialize services. Error: {e}")

startup_event()

def get_embedding_from_api(text: str) -> list:
    """
    This function calls the Hugging Face API to get the vector embedding.
    """
    try:
        # --- THIS IS THE FIX ---
        # We add a `timeout` of 15 seconds to the request.
        # If the Hugging Face API doesn't respond within 15s, this will raise a Timeout exception
        # instead of letting our server hang indefinitely.
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": text, "options": {"wait_for_model": True}},
            timeout=15
        )
        response.raise_for_status() # This will raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()[0]
    
    except requests.exceptions.Timeout:
        print("Error: Hugging Face API call timed out after 15 seconds.")
        raise ConnectionError("The embedding service took too long to respond.")
    except requests.exceptions.RequestException as e:
        print(f"Error from Hugging Face API: {e}")
        raise ConnectionError("Failed to get embedding from Hugging Face API.")


def get_product_recommendations_from_prompt(prompt: str) -> list:
    """Gets recommendations by calling the embedding API and querying Pinecone."""
    if 'pinecone_index' not in models:
        raise ConnectionError("Pinecone service is not initialized.")

    query_vector = get_embedding_from_api(prompt)

    query_results = models['pinecone_index'].query(
        vector=query_vector,
        top_k=6,
        include_metadata=True
    )

    recommended_products = []
    for match in query_results['matches']:
        metadata = match.get('metadata', {})
        title = metadata.get('title', 'this item')
        genai_desc = f"An excellent choice for your home, this {title.lower()} perfectly matches your request."

        product = {
            "uniq_id": match.get('id', ''),
            "title": title,
            "price": f"${metadata.get('price', 0):.2f}",
            "images": [metadata.get('image_url', '')],
            "genai_description": genai_desc,
        }
        recommended_products.append(product)
        
    return recommended_products