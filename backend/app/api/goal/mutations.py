import strawberry
from ...models.core.goal import *
from datetime import datetime
from ..base.types import BaseInput
from ..base.mutations import BaseAuthenticatedMutation  
from typing import Optional,List
from uuid import UUID
from strawberry.types import Info
from .types import GoalType,GoalSuccess,GoalError,GoalListType
from .validator import GoalMutationValidator
from ...utils import db
from ...models.core.user import UserModel
from ...models.associative import CategoryGoalModel
from fastapi import status

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
    categories:List[UUID] 

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
    categories:Optional[List[UUID]] = None

@strawberry.input(description="Input type for deleting a goal.")
class DeleteGoalInput(BaseInput):
    """
    Input type for deleting a goal.
    """
    id:UUID
    
    
# @strawberry.type(description="Goal mutation type")
# class GoalMutation(BaseAuthenticatedMutation[GoalModel,CreateGoalInput,UpdateGoalInput,DeleteGoalInput,GoalSuccess,GoalType]):
#     """
#     Goal mutation type
#     """
#     model = GoalModel
#     success_type = GoalSuccess
#     type = GoalType
    
#     @strawberry.mutation(description="Create a goal")
#     def create(self,input:CreateGoalInput,info:Info) -> GoalSuccess:
#         """
#         Create a goal
#         """
#         return super().create(input,info)

#     @strawberry.mutation(description="Update a goal")
#     def update(self,input:UpdateGoalInput,info:Info) -> GoalSuccess:
#         """
#         Update a goal
#         """
#         return super().update(input,info)
    
#     @strawberry.mutation(description="Delete a goal")
#     def delete(self,input:DeleteGoalInput,info:Info) -> GoalSuccess:
#         """
#         Delete a goal
#         """
#         return super().delete(input,info)
    
    

@strawberry.type
class GoalMutation:
    @strawberry.mutation
    def create(self, input:CreateGoalInput, info:Info) -> GoalSuccess:
        session = db.get_session()
        user:UserModel = info.context.get("user")
        validator = GoalMutationValidator(session=session, input=input, user=user)
        parsed_input = input.to_dict()
        try:
            categories = validator.validate_create_input()
            new_goal = GoalModel(user_id=user.id, 
                                 name=parsed_input["name"],
                                 description=parsed_input["description"],
                                 target=parsed_input["target"],
                                 start_date=parsed_input["start_date"],
                                 end_date=parsed_input["end_date"],
                                 status=parsed_input["status"])
            session.add(new_goal)
            session.flush()
            for category in categories:
                new_goal_category = CategoryGoalModel(goal_id=new_goal.id, category_id=category.id)
                session.add(new_goal_category)
            session.commit()
            session.refresh(new_goal)
            success_data = {
                "code":status.HTTP_201_CREATED,
                "message":"Goal created successfully",
                "values":GoalType(**new_goal.to_dict(), categories=categories)
            }
            return GoalSuccess(**success_data)
        except GoalError as e:
            raise GoalError(message=e.message, code=e.code)
        except Exception as e:
            raise GoalError(message="Failed to create goal", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            session.close()
            
    @strawberry.mutation
    def update(self, input:UpdateGoalInput, info:Info) -> GoalSuccess:
        session = db.get_session()
        user:UserModel = info.context.get("user")
        validator = GoalMutationValidator(session=session, input=input, user=user)
        parsed_input = input.to_dict()
        try:
            goal, categories = validator.validate_update_input()
            if parsed_input.get("name"):
                goal.name = parsed_input["name"]
            if parsed_input.get("description"):
                goal.description = parsed_input["description"]
            if parsed_input.get("target"):
                goal.target = parsed_input["target"]
            if parsed_input.get("start_date"): 
                goal.start_date = parsed_input["start_date"]
            if parsed_input.get("end_date"):
                goal.end_date = parsed_input["end_date"]
            if parsed_input.get("status"):
                goal.status = parsed_input["status"]
            goal.updated_at = sql.func.now()
            session.commit()
            session.refresh(goal)
            success_data = {
                "code":status.HTTP_200_OK,
                "message":"Goal updated successfully",
                "values":GoalType(**goal.to_dict(), categories=categories)
            }
            return GoalSuccess(**success_data)
        except GoalError as e:
            raise GoalError(message=e.message, code=e.code)
        except Exception as e:
            raise GoalError(message="Failed to update goal", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            session.close()
            
    @strawberry.mutation
    def delete(self, input:DeleteGoalInput, info:Info) -> GoalSuccess:
        session = db.get_session()
        user:UserModel = info.context.get("user")
        validator = GoalMutationValidator(session=session, input=input, user=user)
        try:
            goal = validator.validate_delete_input()
            goal.deleted_at = sql.func.now()
            session.commit()
            success_data = {
                "code":status.HTTP_204_NO_CONTENT,
                "message":"Goal deleted successfully",
                "values":None
            }
            return GoalSuccess(**success_data)
        except GoalError as e:
            raise GoalError(message=e.message, code=e.code)
        except Exception as e:
            raise GoalError(message="Failed to delete goal", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            session.close()