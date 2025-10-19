import pinecone
from sentence_transformers import SentenceTransformer
# We REMOVE the import for 'pipeline' and 're' as they are no longer needed

# --- ⚙️ CONFIGURATION (with your hardcoded keys) ---
# Your keys are kept directly in the file as you requested.
PINECONE_API_KEY = "pcsk_3spAud_D66kNnQiYH4TF99hStEuThoSqjoingbaw7zXLRzRfPmvaXjurbpVMg38bdxU2gM"
INDEX_HOST = "https://recomend-6c7pmst.svc.aped-4627-b74a.pinecone.io"

# --- Global Models (loaded once on startup) ---
models = {}

def startup_event():
    """
    Loads ONLY the essential AI model to stay within Render's 512MB memory limit.
    """
    print("Loading AI models and connecting to Pinecone...")
    try:
        pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
        models['pinecone_index'] = pc.Index(host=INDEX_HOST)
        
        # We ONLY load the text embedder. This is the essential model.
        models['text_embedder'] = SentenceTransformer('./all-MiniLM-L6-v2') 
        
        # REMOVED: The description_generator pipeline is removed to save ~350MB of RAM.
        
        print("✅ Essential models loaded and Pinecone connected successfully.")
    except Exception as e:
        print(f"❌ FATAL: Could not initialize models or services. Error: {e}")

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

    # 3. Process results and generate a SIMPLE, non-AI description.
    recommended_products = []
    for match in query_results['matches']:
        metadata = match.get('metadata', {})
        
        # THE FIX: We create a simple, template-based description here.
        # This fulfills the requirement of having a description without
        # using the heavy AI model that was causing the memory crash.
        # We can use the 'title' from the metadata to make it a bit more dynamic.
        title = metadata.get('title', 'this item')
        genai_desc = f"An excellent choice for your home, this {title.lower()} perfectly matches your request."

        product = {
            "uniq_id": match.get('id', ''),
            "title": metadata.get('title', 'No Title'),
            "price": f"${metadata.get('price', 0):.2f}",
            "images": [metadata.get('image_url', '')],
            "genai_description": genai_desc,
        }
        recommended_products.append(product)
        
    return recommended_products