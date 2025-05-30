from ..base import Base
from enum import Enum as PyEnum
from uuid import UUID
from sqlalchemy import Column, String, UUID, ForeignKey,Enum,Float
from sqlalchemy.orm import relationship

class TransactionBudgetModel(Base):
    __tablename__ = "transactions_budgets"
    
    transaction_id = Column(UUID, ForeignKey("transactions.id"), primary_key=True)
    budget_id = Column(UUID, ForeignKey("budgets.id"), primary_key=True)
    amount = Column(Float, nullable=False)
    
    transaction = relationship("TransactionModel", back_populates="transactions_budgets", foreign_keys=[transaction_id])
    budget = relationship("BudgetModel", back_populates="transactions_budgets", foreign_keys=[budget_id])