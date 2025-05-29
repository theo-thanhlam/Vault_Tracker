from ..base import Base
from enum import Enum as PyEnum
from uuid import UUID
from sqlalchemy import Column, String, UUID, ForeignKey,Enum
from sqlalchemy.orm import relationship

class CategoryBudgetModel(Base):
    __tablename__ = "categories_budgets"
    
    category_id = Column(UUID, ForeignKey("categories.id"), primary_key=True)
    budget_id = Column(UUID, ForeignKey("budgets.id"), primary_key=True)
    
    category = relationship("CategoryModel", back_populates="categories_budgets", foreign_keys=[category_id])
    budget = relationship("BudgetModel", back_populates="categories_budgets", foreign_keys=[budget_id])