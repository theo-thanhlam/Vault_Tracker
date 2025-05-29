from ..base import Base
from enum import Enum as PyEnum
from uuid import UUID
from sqlalchemy import Column, String, UUID, ForeignKey,Enum,Float
from sqlalchemy.orm import relationship

class TransactionGoalModel(Base):
    __tablename__ = "transactions_goals"
    
    transaction_id = Column(UUID, ForeignKey("transactions.id"), primary_key=True)
    goal_id = Column(UUID, ForeignKey("goals.id"), primary_key=True)
    amount = Column(Float, nullable=False)
    
    transaction = relationship("TransactionModel", back_populates="transactions_goals", foreign_keys=[transaction_id])
    goal = relationship("GoalModel", back_populates="transactions_goals", foreign_keys=[goal_id])