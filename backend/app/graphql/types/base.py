import strawberry
from uuid import UUID
from datetime import datetime

@strawberry.type
class BaseType:
    id:UUID 
    created_at:datetime 
    deleted_at:datetime 