import strawberry
from ..base.types import BaseSuccess,BaseType, BaseError
from ...models.category import CategoryTypeEnum
from uuid import UUID
from typing import List

@strawberry.type
class CategoryType(BaseType):
    name:str
    type:CategoryTypeEnum
    description:str
    user_id: UUID
    parent_id:UUID | None
    
    
@strawberry.type
class CategorySuccess(BaseSuccess[CategoryType]):
    pass
    
@strawberry.type
class GetCategorySuccess(BaseSuccess[CategoryType]):
    values:List[CategoryType]
    
    
    
@strawberry.type
class CategoryError(BaseError):
    pass