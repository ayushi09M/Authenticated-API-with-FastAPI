from pydantic import BaseModel

# It will provide the structure of the request and response model
# pydantic model.
# It will define how the data should be sent and received from the API endpoints 
class Product(BaseModel):
    name:str
    description:str
    price:float

# Hide informaation like price while creating a product, 
# and show only those information which we want to show
class DisplayProduct(BaseModel):
    name:str
    description:str
    
    class Config:
        orm_mode = True