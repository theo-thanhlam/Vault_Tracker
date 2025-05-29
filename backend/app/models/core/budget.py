from ..base import BaseModel
from sqlalchemy import Column, String, Float, DateTime,sql,UUID,ForeignKey,Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

class BudgetTypeEnum(str, PyEnum):
    FIXED = 'fixed'
    FLEXIBLE = 'flexible'
    ROLLING = 'rolling'
    SAVINGS = 'savings'
    
class BudgetFrequencyEnum(int, PyEnum):
    DAILY = 1
    WEEKLY = 7
    BI_WEEKLY = 14
    MONTHLY = 30
    YEARLY = 365
    
    

class BudgetModel(BaseModel):
    __tablename__ = 'budgets'
    
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"),nullable=False)
    
    type = Column(Enum(BudgetTypeEnum), nullable=True)
    frequency = Column(Enum(BudgetFrequencyEnum), nullable=True)
    start_date = Column(DateTime, default=sql.func.now(), nullable=True)
    end_date = Column(DateTime, default=sql.func.now(), nullable=True)

    budget_user_relationship = relationship("UserModel", back_populates="user_budget_relationship")
    transactions_budgets = relationship("TransactionBudgetModel", back_populates="budget")
    categories_budgets = relationship("CategoryBudgetModel", back_populates="budget")
    
    