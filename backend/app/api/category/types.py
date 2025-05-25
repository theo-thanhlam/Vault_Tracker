import strawberry
from ..base.types import BaseSuccess,BaseType, BaseError, BaseResponse
from ...models.category import CategoryTypeEnum
from uuid import UUID
from typing import List, Optional, Dict
from strawberry.scalars import JSON

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
    
    
    
class CategoryError(BaseError):
    pass

@strawberry.type
class CategoryTypeSum:
    type:str
    total:float

@strawberry.type
class getSumByCategoryTypeSuccess(BaseSuccess[JSON]):
    pass
   
    