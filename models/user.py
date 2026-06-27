from sqlalchemy import Column, Integer, String
from extensions import *

class User(db.Model):
    __tablename__ = 'users'  
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False,index=True)
    password = Column(String(128), nullable=False,index=True)
    phone = Column(String(11), nullable=False,index=True)
    address = Column(String, nullable=False,index=True)