from .base import BaseModel, Field,Relationship
from uuid import UUID
from ..models import UserModel

class TransactionModel(BaseModel, table=True):
    __tablename__="transactions"
    amount:float
    user_id:UUID = Field(foreign_key="users.id")
    
    user:UserModel = Relationship(back_populates="transactions")
    
    