from sqlalchemy import Column, Integer, String
from .database import Base

# It will provide the structure of the database table
# This model act as a blueprint for the databse table
# Database model. 
# It will define how the data should be stored in the database
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)