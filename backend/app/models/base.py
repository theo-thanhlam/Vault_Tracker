from sqlmodel import Field, SQLModel,Relationship
from uuid import UUID, uuid4
from datetime import datetime



class BaseModel(SQLModel):
    id:UUID = Field(default=uuid4, primary_key=True)
    created_at:datetime = Field(default=datetime.now)
    deleted_at:datetime = Field(default=None)
