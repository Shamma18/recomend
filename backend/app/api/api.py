from fastapi import APIRouter
from app.api.endpoints import recommendations, analytics

api_router = APIRouter()

# Include the routers for different functionalities
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])