from sqlalchemy import Column, DateTime, UUID,sql, String
import uuid
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class BaseModel(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, insert_default=uuid.uuid4)
    created_at = Column(DateTime, server_default=sql.func.now())
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)