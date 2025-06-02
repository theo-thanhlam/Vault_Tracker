from ..base import BaseModel
from sqlalchemy import Column, String, Float, DateTime,sql,UUID,ForeignKey,Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum


class GoalProgressStatusEnum(str,PyEnum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"

class GoalModel(BaseModel):
    __tablename__ = 'goals'
    
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    target = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(Enum(GoalProgressStatusEnum))
    user_id = Column(UUID, ForeignKey("users.id"),nullable=False)
    category_id = Column(UUID, ForeignKey("categories.id"),nullable=False)
    
    goal_user_relationship = relationship("UserModel", back_populates="user_goal_relationship")
    goal_category_relationship = relationship("CategoryModel", back_populates="category_goal_relationship")
    
    