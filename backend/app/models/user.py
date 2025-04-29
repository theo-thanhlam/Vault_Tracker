
from .base import BaseModel,Relationship
from ..models import TransactionModel
from typing import List

class UserModel(BaseModel,table=True):
    __tablename__="users"
    
    firstName:str 
    lastName:str
    email:str
    password:str
    
    transactions: List[TransactionModel] = Relationship(back_populates="user")
    
   
