from sqlalchemy import Column, Integer, String
from extensions import *
from flask_login import UserMixin

class User(db.Model,UserMixin):
    __tablename__ = 'users'  
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False,index=True)
    password = Column(String(128), nullable=False,index=True)
    phone = Column(String(11), nullable=False,index=True)
    address = Column(String, nullable=False,index=True)
    date_creat = Column(String(15) , default=get_current_time) 
