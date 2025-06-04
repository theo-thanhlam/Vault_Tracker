import strawberry
from ...models.core.budget import *
from ..base.types import BaseInput
from ..base.mutations import BaseAuthenticatedMutation
from typing import Optional,List
from uuid import UUID
from strawberry.types import Info
from .types import BudgetType,BudgetSuccess,BudgetError
from datetime import datetime



@strawberry.input(description="Input type for creating a budget.")
class CreateBudgetInput(BaseInput):
    """
    Input type for creating a budget.
    """
    name:str
    description:str
    amount:float
    type:BudgetTypeEnum
    frequency:BudgetFrequencyEnum
    start_date:Optional[datetime] = None    
    end_date:Optional[datetime] = None
    category_id:UUID
    
@strawberry.input(description="Input type for updating a budget.")
class UpdateBudgetInput(BaseInput):
    """
    Input type for updating a budget.
    """
    id:UUID
    name:Optional[str] = None
    description:Optional[str] = None
    amount:Optional[float] = None
    type:Optional[BudgetTypeEnum] = None
    frequency:Optional[BudgetFrequencyEnum] = None
    start_date:Optional[datetime] = None
    end_date:Optional[datetime] = None
    category_id:Optional[UUID] = None
@strawberry.input(description="Input type for deleting a budget.")
class DeleteBudgetInput(BaseInput):
    """
    Input type for deleting a budget.
    """
    id:UUID
    
    
@strawberry.type(description="Budget mutation type")
class BudgetMutation(BaseAuthenticatedMutation[BudgetModel,CreateBudgetInput,UpdateBudgetInput,DeleteBudgetInput,BudgetSuccess,BudgetType]):
    """
    Budget mutation type
    """
    model = BudgetModel
    success_type = BudgetSuccess
    type = BudgetType
    
    @strawberry.mutation(description="Create a budget")
    def create(self,input:CreateBudgetInput,info:Info) -> BudgetSuccess:
        """
        Create a budget
        """
        
        return super().create(input,info)
    
    @strawberry.mutation(description="Update a budget")
    def update(self,input:UpdateBudgetInput,info:Info) -> BudgetSuccess:
        """
        """
        return super().update(input,info)
    
    @strawberry.mutation(description="Delete a budget")
    def delete(self,input:DeleteBudgetInput,info:Info) -> BudgetSuccess:
        """
        Delete a budget
        """
        return super().delete(input,info)