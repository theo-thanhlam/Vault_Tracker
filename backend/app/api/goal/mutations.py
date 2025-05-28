import strawberry
from ...models.core.goal import *
from datetime import datetime
from ..base.types import BaseInput
from ..base.mutations import BaseAuthenticatedMutation  
from typing import Optional
from uuid import UUID
from strawberry.types import Info
from .types import GoalType,GoalSuccess,GoalError,GoalListType

@strawberry.input(description="Input type for creating a goal.")
class CreateGoalInput(BaseInput):
    """
    Input type for creating a goal.
    """
    name:str
    description:str
    target:float
    start_date:datetime
    end_date:datetime
    status:GoalProgressStatusEnum

@strawberry.input(description="Input type for updating a goal.")
class UpdateGoalInput(BaseInput):
    """
    Input type for updating a goal.
    """
    id:UUID
    name:Optional[str] = None
    description:Optional[str] = None
    target:Optional[float] = None
    start_date:Optional[datetime] = None
    end_date:Optional[datetime] = None
    status:Optional[GoalProgressStatusEnum] = None

@strawberry.input(description="Input type for deleting a goal.")
class DeleteGoalInput(BaseInput):
    """
    Input type for deleting a goal.
    """
    id:UUID
    
    
@strawberry.type(description="Goal mutation type")
class GoalMutation(BaseAuthenticatedMutation[GoalModel,CreateGoalInput,UpdateGoalInput,DeleteGoalInput,GoalSuccess,GoalType]):
    """
    Goal mutation type
    """
    model = GoalModel
    success_type = GoalSuccess
    type = GoalType
    
    @strawberry.mutation(description="Create a goal")
    def create(self,input:CreateGoalInput,info:Info) -> GoalSuccess:
        """
        Create a goal
        """
        return super().create(input,info)

    @strawberry.mutation(description="Update a goal")
    def update(self,input:UpdateGoalInput,info:Info) -> GoalSuccess:
        """
        Update a goal
        """
        return super().update(input,info)
    
    @strawberry.mutation(description="Delete a goal")
    def delete(self,input:DeleteGoalInput,info:Info) -> GoalSuccess:
        """
        Delete a goal
        """
        return super().delete(input,info)
    
    
    
    
