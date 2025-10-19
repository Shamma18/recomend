from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router

app = FastAPI(title="Product Recommendation API")

# --- THIS IS THE FIX ---
# We are creating a list that explicitly allows BOTH your local development server
# AND your live deployed frontend to make requests.
origins = [
    "http://localhost:3000",  # For running on your computer
    "https://recomend-frontend.onrender.com", # e.g., "https://furniture-ai-app.onrender.com"
]

# This print statement is helpful for debugging in your Render logs.
print(f"Allowing CORS from: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the main router from api.py
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    # Health check endpoint
    return {"message": "Welcome to the Furniture Recommendation AI API"}