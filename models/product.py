from sqlalchemy import Column, Integer, String
from extensions import *

class Product(db.Model):
    __tablename__ = 'products'  
    
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False,index=True)
    price = Column(Integer, nullable=False,index=True)
    description = Column(String, nullable=False,index=True)
    active = Column(String, nullable=False,index=True)
    
   