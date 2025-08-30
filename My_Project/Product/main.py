from fastapi import FastAPI
from . import schemas
from . import models
from .database import engine

# (if you have schemas.py inside a package like Product):
# from Product import schemas
app = FastAPI()

models.Base.metadata.create_all(engine)

@app.post('/product')
def add_product(request: schemas.Product):
    return request