from sqlalchemy import Column, String, DateTime,sql
from .base import Base

class VerificationModel(Base):
    __tablename__="verification_token"
    token = Column(String, primary_key=True)
    created_at = Column(DateTime, nullable=True, server_default=sql.func.now())