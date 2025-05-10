from .base import BaseModel
from sqlalchemy import Column, String, Float, DateTime,sql,UUID,ForeignKey

from sqlalchemy.orm import relationship




class ExpenseModel(BaseModel):
    __tablename__="expenses"

    amount = Column(Float, nullable=False)
    description = Column(String(200))
    category = Column(String(50))
    expense_date = Column(DateTime, default=sql.func.now())
    user_id = Column(UUID, ForeignKey("users.id"),nullable=False)
    
    user = relationship("UserModel", back_populates="expenses")