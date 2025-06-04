from sqlalchemy import Column, DateTime, UUID,sql, String
import uuid
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.inspection import inspect
import datetime


class Base(DeclarativeBase):
    def to_dict(self):
        return {
            field.name: self._cast_value(getattr(self, field.name))
            for field in self.__table__.c
        }
    def _cast_value(self,value):
        if isinstance(value, uuid.UUID):
            return str(value)
        # elif isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
        #     return value.isoformat()
        else:
            return value

        

class BaseModel(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, insert_default=uuid.uuid4)
    created_at = Column(DateTime, server_default=sql.func.now())
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

class AssociativeBaseModel(Base):
    __abstract__ = True
    created_at = Column(DateTime, server_default=sql.func.now())
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
