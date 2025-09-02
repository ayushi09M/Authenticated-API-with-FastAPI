from fastapi import FastAPI, Response, HTTPException
from fastapi import status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from Product import schemas
from Product import models
from Product.database import engine, SessionLocal
from typing import List
from passlib.context import CryptContext

# (if you have schemas.py inside a package like Product):
# from Product import schemas
app = FastAPI()

models.Base.metadata.create_all(engine)

# creating pwd context instance
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Dependency Injection for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

# create
@app.post('/product', status_code=status.HTTP_201_CREATED)
def add_product(request: schemas.Product, db: Session =  Depends(get_db)):
    new_product = models.Product(
        name=request.name ,description=request.description, price=request.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

# read
# get all products
@app.get('/products', response_model = List[schemas.DisplayProduct])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


# get product by id
@app.get('/product/{id}', response_model = schemas.DisplayProduct)
def get_product(id , response: Response ,db: Session = Depends(get_db)):
    product=db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Product with the id {id} is not available')
        # Alternatively, you can use:
        # response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'product not found'}
    return product


# delete 
@app.delete('/product/{id}', status_code=201)
def delete_product(id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {'product deleted successfully': product}


# Update
@app.put('/product/{id}')
def update_product(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        return {'message': 'product not found'}
    product.update(request.dict())
    db.commit()
    return 'product updated successfully'   


# ===========Creating Multiple model and Establishing Relationsip===========================

@app.post('/seller', response_model= schemas.DisplaySeller ,status_code=status.HTTP_201_CREATED)
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hashedpassword = pwd_context.hash(request.password)
    new_seller = models.Seller(
        username=request.username, email=request.email, password=hashedpassword)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller