# ---------------------------------------------------------
# FastAPI Tutorial: Using Example Schemas for Fields & Models
# ---------------------------------------------------------

# 📌 Agenda:
# - Learn how to provide example data for 
#    - individual fields
#    - entire Pydantic model
# - Learn how to use nested models in FastAPI
# - Practice with POST APIs and Swagger UI

from fastapi import FastAPI
from pydantic import BaseModel, Field, HttpUrl
from typing import Set, List

# ---------------------------------------------------------
# 1. Initialize the FastAPI App
# ---------------------------------------------------------
app = FastAPI(title="FastAPI Example Schema Tutorial")


# ---------------------------------------------------------
# 2. Image Model
# ---------------------------------------------------------
# - Nested model example: Product will use Image
# - Demonstrates Field types and validation
class Image(BaseModel):
    url: HttpUrl   # URL type validation
    name: str      # Name/label of the image


# ---------------------------------------------------------
# 3. Product Model
# ---------------------------------------------------------
# - Shows examples for individual fields (Field(example=...))
# - Shows global example for the entire model (model_config/json_schema_extra)
# - Nested model: uses Image
class Product(BaseModel):
    # Example for individual field
    name: str = Field(example="phone")  

    price: int = Field(
        title="Price of the item",
        gt=0,  # must be > 0
        description="Price must be greater than zero",
        example=100  # Example for Swagger UI
    )

    discount: int

    # Example for Set field
    tags: Set[str] = Field(example=["electronics", "phone"])  

    # Nested model
    image: List[Image]

    # Example schema for entire model (Swagger UI shows this as "example")
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Sample Product",
                "price": 150,
                "discount": 10,
                "tags": ["electronics", "gadget"],
                "image": [
                    {"url": "https://example.com/img1.jpg", "name": "Front View"},
                    {"url": "https://example.com/img2.jpg", "name": "Side View"}
                ]
            }
        }
    }



# ---------------------------------------------------------
# 4. API Endpoints
# ---------------------------------------------------------

@app.post("/addproduct")
def add_product(product: Product):
    """
    POST API to add a product.

    Request Body:
    - Product fields include: name, price, discount, tags, and images
    - Shows both field-level and model-level examples in Swagger UI
    """
    return {"message": "✅ Product added successfully!", "data": product}

