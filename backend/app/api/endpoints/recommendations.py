from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas import RecommendationRequest, Product
from app.services import recommendation_service

router = APIRouter()

@router.post("/", response_model=List[Product])
def get_recommendations(request: RecommendationRequest):
    """
    Accepts a user prompt and returns a list of recommended products.
    """
    try:
        if not request.prompt:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
            
        products = recommendation_service.get_product_recommendations_from_prompt(
            prompt=request.prompt
        )
        return products
    except ConnectionError as e:
        # Handle cases where models or Pinecone might not be available
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        # Generic error handler
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred while fetching recommendations.")