from sqlalchemy import Column, Integer, String , ForeignKey
from extensions import *

class Payment(db.Model):
    __tablename__ = 'payments'  
    
    id = Column(Integer, primary_key=True)
    status = Column(String , default='pending')
    price = Column(Integer)
    track_id = Column(String, unique=True, index=True)
    refid = Column(String)
    transaction_id = Column(String)
    card_pan = Column(String)
    date_creat = Column(String(15) , default=get_current_time) 
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    cart = db.relationship('Cart', backref='payments')     
   