import strawberry
from ...models.core.goal import *
from datetime import datetime
from ..base.types import BaseInput
from ..base.mutations import BaseAuthenticatedMutation  
from typing import Optional,List
from uuid import UUID
from strawberry.types import Info
from .types import GoalType,GoalSuccess,GoalError,GoalListType
from ...utils import db
from ...models.core import CategoryModel
from ...models.associative import CategoryGoalModel
from fastapi import status
from ..category.types import CategoryType

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
    categories:List[UUID] 
    status:GoalStatusEnum

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
    categories:List[UUID] 
    status:Optional[GoalStatusEnum] = None

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
        # return super().create(input,info)
        session = db.get_session()
        user = info.context.get("user")
        if not input.categories:
            raise GoalError(message="Categories are required", code=status.HTTP_400_BAD_REQUEST)
        if input.categories:
            categories = session.query(CategoryModel).filter(CategoryModel.id.in_(input.categories)).filter(CategoryModel.user_id==user.id).filter(CategoryModel.deleted_at==None).all()
            if len(categories) != len(input.categories):
                raise GoalError(message="One or more categories not found", code=status.HTTP_404_NOT_FOUND)
        try:
            new_goal_instance = GoalModel(
                user_id=user.id, 
                name=input.name, 
                description=input.description, 
                target=input.target, 
                start_date=input.start_date, 
                end_date=input.end_date, 
                status=input.status
                )
            session.add(new_goal_instance)
            session.flush()
            for category in categories:
                session.add(CategoryGoalModel(category_id=category.id,goal_id=new_goal_instance.id))
            session.commit()
     
            return GoalSuccess(message="Goal created successfully",
                           values=GoalType(**new_goal_instance.to_dict(), categories = [CategoryType(**category.to_dict()) for category in categories]), 
                           code=status.HTTP_201_CREATED)        
        
        except Exception as e:
            session.rollback()
            raise GoalError(message="Error creating goal", code=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()
        
            
    @strawberry.mutation(description="Update a goal")
    def update(self, input: UpdateGoalInput, info: Info) -> GoalSuccess:
        """
        Update a goal and its associated categories.
        
        Args:
            input (UpdateGoalInput): The input data containing goal fields to update
            info (Info): GraphQL context containing the authenticated user
            
        Returns:
            GoalSuccess: Success response with updated goal data
            
        Raises:
            GoalError: If goal not found, unauthorized, or invalid category IDs
        """
        session = db.get_session()
        user = info.context.get("user")
        if not input.categories:
            raise GoalError(message="Categories are required", code=status.HTTP_400_BAD_REQUEST)
        
        # Get the goal instance
        goal = session.get(GoalModel, input.id)
        if not goal or goal.deleted_at:
            raise GoalError(message="Goal not found", code=status.HTTP_404_NOT_FOUND)
            
        # Check ownership
        if user.id != goal.user_id:
            raise GoalError(message="Unauthorized", code=status.HTTP_401_UNAUTHORIZED)
            
        try:
            # Update basic goal fields
            parsed_input = input.to_dict()
            for field, value in parsed_input.items():
                if value is not None and field != 'categories':
                    setattr(goal, field, value)
            
            # Handle category updates if provided
           
                # Verify all categories exist
            categories = session.query(CategoryModel).filter(CategoryModel.id.in_(input.categories)).filter(CategoryModel.user_id==user.id).filter(CategoryModel.deleted_at==None).all()
            if len(categories) != len(input.categories):
                raise GoalError(message="One or more categories not found", code=status.HTTP_400_BAD_REQUEST)
                
                # Remove existing category associations
            session.query(CategoryGoalModel).filter(CategoryGoalModel.goal_id == goal.id).delete()
                
                # Add new category associations
            for category in categories:
                session.add(CategoryGoalModel(category_id=category.id, goal_id=goal.id))
            
            goal.updated_at = datetime.now()
            session.commit()
            session.refresh(goal)
            return GoalSuccess(
                message="Goal updated successfully",
                values=GoalType(**goal.to_dict(), categories = [CategoryType(**category.to_dict()) for category in categories]) , 
                code=status.HTTP_200_OK)
            
            
        except Exception as e:
            session.rollback()
            raise GoalError(message="Error updating goal", code=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()

        
    
    @strawberry.mutation(description="Delete a goal")
    def delete(self,input:DeleteGoalInput,info:Info) -> GoalSuccess:
        """
        Delete a goal
        """
        session = db.get_session()
        user = info.context.get("user")
        goal = session.get(GoalModel, input.id)
        if not goal or goal.deleted_at:
            raise GoalError(message="Goal not found", code=status.HTTP_404_NOT_FOUND)
        if user.id != goal.user_id:
            raise GoalError(message="Unauthorized", code=status.HTTP_401_UNAUTHORIZED)  
        try:
            goal.deleted_at = sql.func.now()
            session.query(CategoryGoalModel).filter(CategoryGoalModel.goal_id == goal.id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise GoalError(message="Error deleting goal", code=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()
        return GoalSuccess(message="Goal deleted successfully", code=status.HTTP_204_NO_CONTENT)
    
    
    
