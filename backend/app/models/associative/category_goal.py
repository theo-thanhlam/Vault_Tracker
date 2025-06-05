from ..base import AssociativeBaseModel
from sqlalchemy import Column, String, Float, DateTime,sql,UUID,ForeignKey,Enum,PrimaryKeyConstraint

from sqlalchemy.orm import relationship
from enum import Enum as PyEnum


class CategoryGoalModel(AssociativeBaseModel):
    __tablename__ = "categories_goals"

    category_id = Column(UUID, ForeignKey("categories.id"), primary_key=True    )
    goal_id = Column(UUID, ForeignKey("goals.id"), primary_key=True)
    
    __table_args__ = (
        PrimaryKeyConstraint(category_id, goal_id),{}   
    )
    
    category_goal_association = relationship("CategoryModel", back_populates="category_goal_association")
    goal_category_association = relationship("GoalModel", back_populates="goal_category_association")
