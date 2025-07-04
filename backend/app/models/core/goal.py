from ..base import BaseModel
from sqlalchemy import Column, String, Float, DateTime,sql,UUID,ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum


class GoalStatusEnum(str,PyEnum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    CUSTOM = "custom"

class GoalModel(BaseModel):
    __tablename__ = 'goals'
    
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    target = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(SQLAlchemyEnum(GoalStatusEnum))
    user_id = Column(UUID, ForeignKey("users.id"),nullable=False)
    # category_id = Column(UUID, ForeignKey("categories.id"),nullable=True)
    
    goal_user_relationship = relationship("UserModel", back_populates="user_goal_relationship")
    # goal_category_relationship = relationship("CategoryModel", back_populates="category_goal_relationship")
    # goal_transaction_association = relationship("TransactionGoalModel", back_populates="goal_transaction_association")
    goal_category_association = relationship("CategoryGoalModel", back_populates="goal_category_association")
    
    