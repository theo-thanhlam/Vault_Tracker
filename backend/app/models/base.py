from sqlalchemy import Column, DateTime, UUID,sql
import uuid
from sqlalchemy.orm import DeclarativeBase

class BaseModel(DeclarativeBase):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, server_default=sql.func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=sql.func.now())
    deleted_at = Column(DateTime, nullable=True, onupdate=sql.func.now())