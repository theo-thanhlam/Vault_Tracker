from .base import BaseModel
from sqlalchemy import Column, String, Float, DateTime,sql,UUID,ForeignKey,Enum

from sqlalchemy.orm import relationship
from enum import Enum as PyEnum



class TransactionType(str,PyEnum):
    INCOME = 'income'
    EXPENSE = 'expense'
    OTHER = 'other'

transaction_type_list = [t.value for t in TransactionType]


class TransactionModel(BaseModel):
    __tablename__="transactions"

    amount = Column(Float, nullable=False)
    description = Column(String(200))
    category = Column(String(50))
    date = Column(DateTime, default=sql.func.now())
    user_id = Column(UUID, ForeignKey("users.id"),nullable=False)
    type = Column(Enum(TransactionType))
    
    user = relationship("UserModel", back_populates="transactions")