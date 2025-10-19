import pinecone
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import re

# --- ⚙️ CORRECTED CONFIGURATION ---
# We ONLY need the API Key and the Index Host for a serverless index.
PINECONE_API_KEY = "pcsk_3spAud_D66kNnQiYH4TF99hStEuThoSqjoingbaw7zXLRzRfPmvaXjurbpVMg38bdxU2gM"
INDEX_HOST = "https://recomend-6c7pmst.svc.aped-4627-b74a.pinecone.io" 
# The PINECONE_ENVIRONMENT variable has been removed.

# --- Global Models (loaded once on startup) ---
models = {}

def startup_event():
    """Loads all necessary AI models and connects to services when the app starts."""
    print("Loading AI models and connecting to Pinecone...")
    try:
        from pinecone import Pinecone
        pc = Pinecone(api_key=PINECONE_API_KEY)
        models['pinecone_index'] = pc.Index(host=INDEX_HOST)
        
        # Load models locally to avoid download issues
        models['text_embedder'] = SentenceTransformer('./all-MiniLM-L6-v2') 
        models['description_generator'] = pipeline('text-generation', model='distilgpt2')
        print(" Models loaded and Pinecone connected successfully.")
    except Exception as e:
        print(f" FATAL: Could not initialize models or services. Error: {e}")

# Load models when the application starts
startup_event()

# --- Main Service Function ---
def get_product_recommendations_from_prompt(prompt: str) -> list:
    if 'pinecone_index' not in models or 'text_embedder' not in models:
        raise ConnectionError("AI services are not initialized. Please check server logs.")

    # 1. Create a 384-dimension vector for the user's search prompt.
    query_vector = models['text_embedder'].encode(prompt).tolist()

    # 2. Query the Pinecone index.
    query_results = models['pinecone_index'].query(
        vector=query_vector,
        top_k=6,
        include_metadata=True
    )

    # 3. Process results and generate clean, non-repetitive descriptions.
    recommended_products = []
    for match in query_results['matches']:
        metadata = match.get('metadata', {})
        
        gen_prompt = (
            f"Describe this product in one creative sentence for a customer who wants '{prompt}': {metadata.get('title', 'product')}"
        )
        
        results = models['description_generator'](
            gen_prompt,
            max_new_tokens=35,
            num_return_sequences=1,
            truncation=True,
            pad_token_id=models['description_generator'].tokenizer.eos_token_id
        )
        
        raw_text = results[0]['generated_text'].replace(gen_prompt, "").strip()
        
        first_sentence_match = re.search(r'[^.!?]*[.!?]', raw_text)
        if first_sentence_match:
            genai_desc = first_sentence_match.group(0).strip()
        else:
            genai_desc = raw_text if raw_text else "A great choice to meet your needs."

        product = {
            "uniq_id": match.get('id', ''),
            "title": metadata.get('title', 'No Title'),
            "price": f"${metadata.get('price', 0):.2f}",
            "images": [metadata.get('image_url', '')],
            "genai_description": genai_desc,
        }
        recommended_products.append(product)
        
    return recommended_products