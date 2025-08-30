from fastapi import FastAPI
from pydantic import BaseModel, Field

# 1. Define Fields with Meta Data using Field class (title, description, example, default value etc.)
# 2. Simple Post API with Request Body
# 3. Post API with Request Body, path parameters, query parameter & extra processing

# 4. Post API with multiple BaseModel (Pydantic models) 
# ---------------------------------------------------------------------------------------------- 

#  Define Pydantic models for request bodies
class Profile(BaseModel):
    name: str
    age: int
    city: str


class Product(BaseModel):
    name: str
    price: int = Field(title="Price of the item", gt=0,
                    description="Price must be greater than zero", example=100)   
    discount: int
    discounted_price: float = None

class User(BaseModel):
    name: str
    email: str

app = FastAPI()

# 1. Simple Request Body
@app.post("/adduser")
def addUser(profile: Profile):
    # return {"message": "User added successfully!"}
    return profile

# 2. Request Body with  path parameters, query parameter & extra processing
@app.post("/addproduct/{product_id}")
def addproduct(product: Product, prodcut_id: int, categoy:str):
    product.discounted_price = product.price - (product.price * product.discount / 100)
    return {"product_id": prodcut_id,"product":product, "category":categoy}

# 3. Post API with multiple BaseModel (Pydantic models)
@app.post("/purchase")
def purchase(user:User, product: Product):
    return {"user": user, "product": product}

