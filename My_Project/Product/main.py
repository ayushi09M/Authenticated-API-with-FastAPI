from fastapi import FastAPI
import schemas

# (if you have schemas.py inside a package like Product):
# from Product import schemas
app = FastAPI()

@app.post('/product')
def add_product(request: schemas.Product):
    return request