from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyticsData
from app.services import analytics_service

# Create a new router object. This will be included in the main app.
router = APIRouter()

@router.get("/", response_model=AnalyticsData)
def get_analytics():
    """
    Defines the GET /api/analytics/ endpoint.
    It returns analytics calculated from the product dataset.
    The `response_model=AnalyticsData` ensures the output matches our Pydantic schema.
    """
    try:
        # Call the service function that does the actual work of reading the CSV and calculating stats.
        analytics_data = analytics_service.generate_analytics()
        return analytics_data
    except FileNotFoundError as e:
        # Specifically handle the case where the cleaned_products.csv file is missing.
        print(f"ERROR in analytics endpoint: {e}")
        raise HTTPException(status_code=404, detail="Analytics data file not found. Please process the data first.")
    except Exception as e:
        # Handle any other unexpected errors during the process.
        print(f"An unexpected error occurred in the analytics endpoint: {e}")
        raise HTTPException(status_code=500, detail="Could not generate analytics due to an internal server error.")