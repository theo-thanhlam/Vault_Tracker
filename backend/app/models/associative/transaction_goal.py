from ..base import AssociativeBaseModel
from sqlalchemy import Column, String, Float, DateTime,sql,UUID,ForeignKey,Enum

from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

class TransactionGoalModel(AssociativeBaseModel):
    __tablename__ = "transactions_goals"

    transaction_id = Column(UUID, ForeignKey("transactions.id"), nullable=False)
    goal_id = Column(UUID, ForeignKey("goals.id"), nullable=False)
    amount = Column(Float, nullable=False)
    
    __mapper_args__ = {
        "primary_key": [transaction_id, goal_id]
    }

    transaction_goal_association = relationship("TransactionModel", back_populates="transaction_goal_association")
    goal_transaction_association = relationship("GoalModel", back_populates="goal_transaction_association")