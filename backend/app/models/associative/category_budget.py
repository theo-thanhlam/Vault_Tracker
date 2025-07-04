from ..base import AssociativeBaseModel
from sqlalchemy import Column, String, Float, DateTime,sql,UUID,ForeignKey,Enum,PrimaryKeyConstraint

from sqlalchemy.orm import relationship
from enum import Enum as PyEnum


class CategoryBudgetModel(AssociativeBaseModel):
    __tablename__ = "categories_budgets"

    category_id = Column(UUID, ForeignKey("categories.id"), primary_key=True)
    budget_id = Column(UUID, ForeignKey("budgets.id"), primary_key=True)
    __table_args__ = (
        PrimaryKeyConstraint(category_id, budget_id),{}
    )
    
    category_budget_association = relationship("CategoryModel", back_populates="category_budget_association")
    budget_category_association = relationship("BudgetModel", back_populates="budget_category_association")
    