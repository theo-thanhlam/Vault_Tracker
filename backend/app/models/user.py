from .base import BaseModel
from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

class UserRole(str, PyEnum):
    USER = "user"
    MANAGER = "manager"
    ADMIN = "admin"


class UserModel(BaseModel):
    __tablename__="users"
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    expenses = relationship("ExpenseModel",back_populates="user", cascade="all, delete-orphan")
