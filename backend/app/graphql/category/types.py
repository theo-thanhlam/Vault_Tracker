import strawberry
from ..baseType import BaseType
from ...models.category import CategoryTypeEnum
from uuid import UUID
from datetime import datetime

@strawberry.type
class CategoryType(BaseType):
    name:str
    type:CategoryTypeEnum
    user_id: UUID
    parent_id:UUID | None
    
    