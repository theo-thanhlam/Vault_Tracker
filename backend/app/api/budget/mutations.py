import strawberry
from ...models.core.budget import *
from ..base.types import BaseInput
from ..base.mutations import BaseAuthenticatedMutation
from typing import Optional
from uuid import UUID
from strawberry.types import Info
from .types import BudgetType,BudgetSuccess,BudgetError
from datetime import datetime
from fastapi import status
from ...models.core.user import UserModel
from .validator import BudgetMutationValidator
from ...utils import db
from typing import List 
from ...models.associative import CategoryBudgetModel

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
    categories:List[UUID] 
    
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
    categories:Optional[List[UUID]] = None
    
@strawberry.input(description="Input type for deleting a budget.")
class DeleteBudgetInput(BaseInput):
    """
    Input type for deleting a budget.
    """
    id:UUID
    
    
# @strawberry.type(description="Budget mutation type")
# class BudgetMutation(BaseAuthenticatedMutation[BudgetModel,CreateBudgetInput,UpdateBudgetInput,DeleteBudgetInput,BudgetSuccess,BudgetType]):
#     """
#     Budget mutation type
#     """
#     model = BudgetModel
#     success_type = BudgetSuccess
#     type = BudgetType
    
#     @strawberry.mutation(description="Create a budget")
#     def create(self,input:CreateBudgetInput,info:Info) -> BudgetSuccess:
#         """
#         Create a budget
#         """
#         return super().create(input,info)
    
#     @strawberry.mutation(description="Update a budget")
#     def update(self,input:UpdateBudgetInput,info:Info) -> BudgetSuccess:
#         """
#         """
#         return super().update(input,info)
    
#     @strawberry.mutation(description="Delete a budget")
#     def delete(self,input:DeleteBudgetInput,info:Info) -> BudgetSuccess:
#         """
#         Delete a budget
#         """
#         return super().delete(input,info)

@strawberry.type
class BudgetMutation:
    @strawberry.mutation
    def create(self, input:CreateBudgetInput, info:Info) -> BudgetSuccess:
        session = db.get_session()
        user:UserModel = info.context.get("user")
        validator = BudgetMutationValidator(session=session, input=input, user=user)
        parsed_input = input.to_dict()
        try:
            categories = validator.validate_create_input()
            new_budget = BudgetModel(user_id=user.id, 
                                     name=parsed_input["name"],
                                     description=parsed_input["description"],
                                     amount=parsed_input["amount"],
                                     type=parsed_input["type"],
                                     frequency=parsed_input["frequency"],
                                     start_date=parsed_input["start_date"],
                                     end_date=parsed_input["end_date"])
            
            session.add(new_budget)
            session.flush()
            for category in categories:
                new_budget_category = CategoryBudgetModel(budget_id=new_budget.id, category_id=category.id)
                session.add(new_budget_category)
            session.commit()
            session.refresh(new_budget) 
           
            success_data = {
                "code":status.HTTP_201_CREATED,
                "message":"Budget created successfully",
                "values":BudgetType(**new_budget.to_dict(), categories = categories)
            }
            return BudgetSuccess(**success_data)
        except BudgetError as e:    
            raise BudgetError(message=e.message, code=e.code)
        except Exception as e:
            raise BudgetError(message="Failed to create budget", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            session.close()

    @strawberry.mutation
    def update(self, input: UpdateBudgetInput, info: Info) -> BudgetSuccess:
        session = db.get_session()
        user: UserModel = info.context.get("user")
        validator = BudgetMutationValidator(session=session, input=input, user=user)
        parsed_input = input.to_dict()
        
        try:
            budget, categories = validator.validate_update_input()
            
            # Update budget fields if provided
            if parsed_input.get("name"):
                budget.name = parsed_input["name"]
            if parsed_input.get("description"):
                budget.description = parsed_input["description"]
            if parsed_input.get("amount"):
                budget.amount = parsed_input["amount"]
            if parsed_input.get("type"):
                budget.type = parsed_input["type"]
            if parsed_input.get("frequency"):
                budget.frequency = parsed_input["frequency"]
            if parsed_input.get("start_date"):
                budget.start_date = parsed_input["start_date"]
            if parsed_input.get("end_date"):
                budget.end_date = parsed_input["end_date"]
            budget.updated_at = sql.func.now()
            # Update categories if provided
            if parsed_input.get("categories"):
                # Remove existing category associations
                session.query(CategoryBudgetModel).filter(
                    CategoryBudgetModel.budget_id == budget.id
                ).delete()
                
                # Add new category associations
                for category in categories:
                    new_budget_category = CategoryBudgetModel(
                        budget_id=budget.id,
                        category_id=category.id
                    )
                    session.add(new_budget_category)

            session.commit()
            session.refresh(budget)

            success_data = {
                "code": status.HTTP_200_OK,
                "message": "Budget updated successfully",
                "values": BudgetType(**budget.to_dict(), categories=categories)
            }
            return BudgetSuccess(**success_data)
        except BudgetError as e:
            raise BudgetError(message=e.message, code=e.code)
        except Exception as e:
            raise BudgetError(message="Failed to update budget", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            session.close()

    @strawberry.mutation
    def delete(self, input: DeleteBudgetInput, info: Info) -> BudgetSuccess:
        session = db.get_session()
        user: UserModel = info.context.get("user")
        validator = BudgetMutationValidator(session=session, input=input, user=user)
        
        try:
            budget = validator.validate_delete_input()
            
            # Delete associated category relationships first
            session.query(CategoryBudgetModel).filter(
                CategoryBudgetModel.budget_id == budget.id
            ).delete()
            
            # Delete the budget
            budget.deleted_at = sql.func.now()
            session.commit()

            success_data = {
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Budget deleted successfully",
                "values": None
            }
            return BudgetSuccess(**success_data)
        except BudgetError as e:
            raise BudgetError(message=e.message, code=e.code)
        except Exception as e:
            raise BudgetError(message="Failed to delete budget", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            session.close()