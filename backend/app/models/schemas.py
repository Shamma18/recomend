from pydantic import BaseModel
from typing import List, Dict

# Schema for the incoming request from the frontend
class RecommendationRequest(BaseModel):
    prompt: str

# Schema for the product data sent back to the frontend
class Product(BaseModel):
    uniq_id: str
    title: str
    price: str
    images: List[str]
    genai_description: str

# Schema for the analytics data
class AnalyticsData(BaseModel):
    total_products: int
    average_price: float
    products_by_category: Dict[str, int]