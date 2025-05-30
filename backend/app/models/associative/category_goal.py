from ..base import Base
from enum import Enum as PyEnum
from uuid import UUID
from sqlalchemy import Column, String, UUID, ForeignKey,Enum
from sqlalchemy.orm import relationship

class CategoryGoalModel(Base):
    __tablename__ = "categories_goals"
    
    category_id = Column(UUID, ForeignKey("categories.id"), primary_key=True)
    goal_id = Column(UUID, ForeignKey("goals.id"), primary_key=True)
    
    category = relationship("CategoryModel", back_populates="categories_goals", foreign_keys=[category_id])
    goal = relationship("GoalModel", back_populates="categories_goals", foreign_keys=[goal_id])