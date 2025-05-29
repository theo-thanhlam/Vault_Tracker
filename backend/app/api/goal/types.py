import strawberry
from ..base.types import BaseSuccess,BaseType,BaseError,BaseResponse
from ...models.core import GoalProgressStatusEnum
from typing import List,Optional
from datetime import datetime   
from uuid import UUID
from ..category.types import CategoryType
@strawberry.type(description="Goal type")
class GoalType(BaseType):
    """
    Goal type
    """
    name:str
    description:str
    target:float
    start_date:datetime
    end_date:datetime
    status:GoalProgressStatusEnum
    user_id:UUID
    categories:List[CategoryType]
    
@strawberry.type(description="Goal success type")
class GoalSuccess(BaseSuccess[GoalType]):
    """
    Goal success type
    """
    pass

@strawberry.type(description="Goal error type") 
class GoalError(BaseError):
    """
    Goal error type
    """
    pass

@strawberry.type(description="Goal list type")
class GoalListType(BaseType):
    """
    Goal list type
    """
    goals:List[GoalType]
    
    
    