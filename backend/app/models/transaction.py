from .base import BaseModel
from sqlalchemy import Column, String, Float, DateTime,sql,UUID,ForeignKey,Enum

from sqlalchemy.orm import relationship
from enum import Enum as PyEnum



class TransactionTypeEnum(str,PyEnum):
    INCOME = 'income'
    EXPENSE = 'expense'
    OTHER = 'other'

transaction_type_list = [t.value for t in TransactionTypeEnum]


class TransactionModel(BaseModel):
    __tablename__="transactions"

    amount = Column(Float, nullable=False)
    description = Column(String(200))
    category_id = Column(UUID, ForeignKey("categories.id"))
    date = Column(DateTime, default=sql.func.now())
    user_id = Column(UUID, ForeignKey("users.id"),nullable=False)
    type = Column(Enum(TransactionTypeEnum))
    
    transaction_user_relationship = relationship("UserModel", back_populates="user_transaction_relationship")
    transaction_category_relationship = relationship("CategoryModel", back_populates="category_transaction_relationship")
    