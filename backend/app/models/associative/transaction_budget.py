from ..base import AssociativeBaseModel
from sqlalchemy import Column, String, Float, DateTime,sql,UUID,ForeignKey,Enum

from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

class TransactionBudgetModel(AssociativeBaseModel):
    __tablename__ = "transactions_budgets"

    transaction_id = Column(UUID, ForeignKey("transactions.id"), nullable=False)
    budget_id = Column(UUID, ForeignKey("budgets.id"), nullable=False)
    amount = Column(Float, nullable=False)
    
    __mapper_args__ = {
        "primary_key": [transaction_id, budget_id]
    }

    transaction_budget_association = relationship("TransactionModel", back_populates="transaction_budget_association")
    budget_transaction_association = relationship("BudgetModel", back_populates="budget_transaction_association")