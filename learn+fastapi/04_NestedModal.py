from fastapi import FastAPI
from pydantic import BaseModel, Field, HttpUrl
from typing import Set, List

app = FastAPI()

# ----------------------------
# 1. Image Model
# ----------------------------
# - Represents an image with a URL and a name.
# - Used inside Product (Nested Model).
class Image(BaseModel):
    url: HttpUrl   # Validated URL type (e.g., "https://example.com/img.jpg")
    name: str      # Name/label of the image


# ----------------------------
# 2. Product Model
# ----------------------------
# - Demonstrates Nested Model (uses Image inside).
# - Demonstrates Set (for unique tags).
# - Demonstrates validation with Field().
class Product(BaseModel):
    name: str
    price: int = Field(
        title="Price of the item",
        gt=0,                               # validation: must be > 0
        description="Price must be greater than zero",
        example=100                         # API docs example
    )
    discount: int
    tags: Set[str] = set()                  # Set ensures uniqueness (no duplicate tags)
    image: List[Image]                      # List of nested Image objects

# ----------------------------
# 3. Offer Model
# ----------------------------
# - Demonstrates Deeply Nested Model (uses Product inside).
# - An offer can have multiple products.
class Offer(BaseModel):
    name: str
    description: str
    price: float
    products: List[Product]                 # List of nested Product objects


# ----------------------------
# 4. API Endpoints
# ----------------------------

@app.post("/addproduct")
def add_product(product: Product):
    """
    POST API to add a product.
    - Body contains product details.
    - Product includes name, price, discount, tags, and images.
    """
    return {"message": "Product added successfully", "data": product}


@app.post("/addoffer")
def add_offer(offer: Offer):
    """
    POST API to add an offer.
    - Body contains offer details.
    - Offer includes multiple products.
    """
    return {"message": "Offer added successfully", "data": offer}
