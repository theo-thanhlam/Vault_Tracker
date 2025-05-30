from ..base import Base
from enum import Enum as PyEnum
from uuid import UUID
from sqlalchemy import Column, String, UUID, ForeignKey,Enum,Float
from sqlalchemy.orm import relationship

class TransactionCategoryModel(Base):
    __tablename__ = "transactions_categories"
    
    transaction_id = Column(UUID, ForeignKey("transactions.id"), primary_key=True)
    category_id = Column(UUID, ForeignKey("categories.id"), primary_key=True)
    amount = Column(Float, nullable=False)
    
    transaction = relationship("TransactionModel", back_populates="transactions_categories", foreign_keys=[transaction_id])
    category = relationship("CategoryModel", back_populates="transactions_categories", foreign_keys=[category_id])