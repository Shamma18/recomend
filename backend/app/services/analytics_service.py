import pandas as pd
from app.models.schemas import AnalyticsData

# The path to the data file, relative to the root of the 'backend' folder
DATA_FILE_PATH = "data/cleaned_products.csv"

def generate_analytics() -> AnalyticsData:
    """Reads the product data and computes basic analytics."""
    try:
        df = pd.read_csv(DATA_FILE_PATH)
    except FileNotFoundError:
        # This error will be caught by the endpoint and sent to the frontend
        raise RuntimeError(f"Analytics data file not found at '{DATA_FILE_PATH}'")

    total_products = len(df)
    average_price = df['price'].mean()
    products_by_category = df['categories'].value_counts().to_dict()

    return AnalyticsData(
        total_products=total_products,
        average_price=average_price,
        products_by_category=products_by_category
    )