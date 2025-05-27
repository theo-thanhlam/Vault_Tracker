from ..base import Base
from enum import Enum as PyEnum
from uuid import UUID
from sqlalchemy import Column, String, UUID, ForeignKey,Enum
from sqlalchemy.orm import relationship


class AuthProviderName(str,PyEnum):
    GOOGLE = "google"
    


class AuthProviderModel(Base):
    __tablename__ = "auth_providers"
    
    id = Column(String, primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    name = Column(Enum(AuthProviderName))
    

    users_with_this_provider = relationship(
        "UserModel",
        back_populates="auth_provider",
        primaryjoin="AuthProviderModel.id==UserModel.auth_provider_id",
        foreign_keys="UserModel.auth_provider_id"
    )