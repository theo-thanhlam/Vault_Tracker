import strawberry
from ..base.types import BaseSuccess,BaseType,BaseError,BaseResponse
from ...models.core.budget import *
from typing import List,Optional
from uuid import UUID
from datetime import datetime
from ..category.types import CategoryType

@strawberry.type(description="Budget type")
class BudgetType(BaseType):
    """
    Budget type
    """
    id:UUID
    name:str
    description:str
    amount:float
    type:BudgetTypeEnum
    frequency:BudgetFrequencyEnum
    start_date:Optional[datetime] = None
    end_date:Optional[datetime] = None
    user_id:UUID
    categories:Optional[List[CategoryType]] = None

@strawberry.type(description="Budget success type")
class BudgetSuccess(BaseSuccess[BudgetType]):
    """
    Budget success type
    """
    pass

class BudgetError(BaseError):
    """
    Budget error type
    """
    pass

@strawberry.type(description="Budget list success type")
class GetBudgetSuccess(BaseSuccess[List[BudgetType]]):
    """
    Get budget success type
    """
    values:List[BudgetType]