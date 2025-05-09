from sqlalchemy import Column, String, DateTime,sql,Enum
from .base import Base
from enum import Enum as PyEnum



class TokenType(str, PyEnum):
   REGISTER = "REGISTER"
   LOGIN = "LOGIN"
#    GOOGLE_LOGIN = ""

class TokenModel(Base):
    __tablename__="verification_token"
    token = Column(String, primary_key=True)
    created_at = Column(DateTime, nullable=True, server_default=sql.func.now())
    type = Column(Enum(TokenType), nullable=True)