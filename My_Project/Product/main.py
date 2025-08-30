from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from . import schemas
from . import models
from .database import engine, SessionLocal

# (if you have schemas.py inside a package like Product):
# from Product import schemas
app = FastAPI()

models.Base.metadata.create_all(engine)

# Dependency Injection for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

# create
@app.post('/product')
def add_product(request: schemas.Product, db: Session =  Depends(get_db)):
    new_product = models.Product(
        name=request.name ,description=request.description, price=request.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

# read
# get all products
@app.get('/products')
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


# get product by id
@app.get('/product/{id}')
def get_product(id , db: Session = Depends(get_db)):
    product=db.query(models.Product).filter(models.Product.id == id).first()
    return product


# delete 
@app.delete('/product/{id}')
def delete_product(id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {'product deleted successfully': product}
