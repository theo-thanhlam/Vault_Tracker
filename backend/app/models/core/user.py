from ..base import BaseModel
from sqlalchemy import Column, String, Enum,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

class UserRoleEnum(str, PyEnum):
    USER = "user"
    MANAGER = "manager"
    ADMIN = "admin"


class UserModel(BaseModel):
    __tablename__="users"
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    
    email_verified = Column(Boolean, default= False)
    auth_provider_id = Column(String, ForeignKey("auth_providers.id"), nullable=True)
    
    auth_provider = relationship(
        "AuthProviderModel",
        back_populates="users_with_this_provider",
        foreign_keys=[auth_provider_id]
    )

    user_transaction_relationship = relationship("TransactionModel",back_populates="transaction_user_relationship", cascade="all, delete-orphan")
    user_categories_relationship = relationship("CategoryModel", back_populates="category_user_relationship", cascade="all, delete-orphan")
    user_goal_relationship = relationship("GoalModel", back_populates="goal_user_relationship", cascade="all, delete-orphan")
    user_budget_relationship = relationship("BudgetModel", back_populates="budget_user_relationship", cascade="all, delete-orphan")

