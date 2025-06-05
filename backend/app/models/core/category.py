
from ..base import BaseModel
from enum import Enum as PyEnum
from uuid import UUID
from sqlalchemy import Column, String, UUID, ForeignKey,Enum
from sqlalchemy.orm import relationship


class CategoryTypeEnum(str,PyEnum):
    EXPENSE = "expense"
    INCOME = 'income'
    EQUITY = "equity"
    LIABILITY = "liability"
    ASSET = "asset"
    OTHER = "other"

category_type_list = [c.value for c in CategoryTypeEnum]

class CategoryModel(BaseModel):
    __tablename__ = "categories"
    
    name = Column(String)
    type = Column(Enum(CategoryTypeEnum), default=CategoryTypeEnum.OTHER)
    description = Column(String, nullable=True)
    user_id = Column(UUID, ForeignKey("users.id"),nullable=False)
    parent_id = Column(UUID, ForeignKey("categories.id"), nullable=True)
    
    # category_budget_relationship = relationship("BudgetModel", back_populates="budget_category_relationship")
    category_transaction_relationship = relationship("TransactionModel", back_populates="transaction_category_relationship")
    category_user_relationship = relationship("UserModel", back_populates="user_categories_relationship")
    # category_goal_relationship = relationship("GoalModel", back_populates="goal_category_relationship")
    self_relationship = relationship("CategoryModel", innerjoin=True)
    
    category_budget_association = relationship("CategoryBudgetModel", back_populates="category_budget_association")
    category_goal_association = relationship("CategoryGoalModel", back_populates="category_goal_association")
    
    
            
    
