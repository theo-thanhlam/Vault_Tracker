import strawberry
from ...models import *
from ..base.types import BaseInput
from ..base.mutations import BaseAuthenticatedMutation
from typing import Optional,List
from uuid import UUID
from strawberry.types import Info
from .types import BudgetType,BudgetSuccess,BudgetError
from datetime import datetime
from ...utils import db
from fastapi import status  
from ..category.types import CategoryType

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
    categories:List[UUID] = None
    
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
    categories:List[UUID] 
    
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
        session = db.get_session()
        user = info.context.get("user")
        if not input.categories:
            raise BudgetError(message="Categories are required", code=status.HTTP_400_BAD_REQUEST)
        if input.categories:
            categories = session.query(CategoryModel).filter(CategoryModel.id.in_(input.categories)).filter(CategoryModel.user_id==user.id).filter(CategoryModel.deleted_at==None).all()
            if len(categories) != len(input.categories):
                raise BudgetError(message="One or more categories not found", code=status.HTTP_404_NOT_FOUND)
        try:
            new_budget_instance = BudgetModel(
                user_id=user.id,
                name=input.name,
                description=input.description,
                amount=input.amount,
                type=input.type,
                frequency=input.frequency,
                start_date=input.start_date,
                end_date=input.end_date
            )
            session.add(new_budget_instance)
            session.flush()
            session.refresh(new_budget_instance)
            
            if input.categories:
                for category in categories:
                    session.add(CategoryBudgetModel(category_id=category.id,budget_id=new_budget_instance.id))
            session.commit()
            session.refresh(new_budget_instance)
            return BudgetSuccess(
                message="Budget created successfully",
                values=BudgetType(**new_budget_instance.to_dict(), categories = [CategoryType(**category.to_dict()) for category in categories]), 
                code=status.HTTP_201_CREATED)

        except Exception as e:
            session.rollback()
        finally:
        
            session.close()
    
    @strawberry.mutation(description="Update a budget")
    def update(self,input:UpdateBudgetInput,info:Info) -> BudgetSuccess:
        """
        """
        session = db.get_session()
        user = info.context.get("user")
        if not input.categories:
            raise BudgetError(message="Categories are required", code=status.HTTP_400_BAD_REQUEST)
        budget = session.get(BudgetModel,input.id)
        if not budget or budget.deleted_at:
            raise BudgetError(message="Budget not found", code=status.HTTP_404_NOT_FOUND)
        
        if user.id != budget.user_id:
            raise BudgetError(message="Unauthorized", code=status.HTTP_401_UNAUTHORIZED)
        
        try:
            parsed_input = input.to_dict()
            for field,value in parsed_input.items():
                if value is not None and field != 'categories':
                    setattr(budget,field,value)
            
            if input.categories:
                categories = session.query(CategoryModel).filter(CategoryModel.id.in_(input.categories)).filter(CategoryModel.user_id==user.id).filter(CategoryModel.deleted_at==None).all()
                if len(categories) != len(input.categories):
                    raise BudgetError(message="One or more categories not found", code=status.HTTP_404_NOT_FOUND)
                
                session.query(CategoryBudgetModel).filter(CategoryBudgetModel.budget_id==budget.id).delete()
                
                for category in categories:
                    session.add(CategoryBudgetModel(category_id=category.id,budget_id=budget.id))
            else:
                session.query(CategoryBudgetModel).filter(CategoryBudgetModel.budget_id==budget.id).delete()
            budget.updated_at = datetime.now()
            session.commit()
            session.refresh(budget)
            return BudgetSuccess(
                message="Budget updated successfully",
                values=BudgetType(**budget.to_dict(), categories = [CategoryType(**category.to_dict()) for category in categories]) , 
                code=status.HTTP_200_OK)
                    
                    
        except Exception as e:
            session.rollback()
            raise BudgetError(message="Error updating budget", code=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()
            
       
            
    
    @strawberry.mutation(description="Delete a budget")
    def delete(self,input:DeleteBudgetInput,info:Info) -> BudgetSuccess:
        """
        Delete a budget
        """
        session = db.get_session()
        user = info.context.get("user")
        budget = session.get(BudgetModel,input.id)
        if not budget or budget.deleted_at:
            raise BudgetError(message="Budget not found", code=status.HTTP_404_NOT_FOUND)
        
        if user.id != budget.user_id:
            raise BudgetError(message="Unauthorized", code=status.HTTP_401_UNAUTHORIZED)
        
        try:
            budget.deleted_at = sql.func.now()
            session.query(CategoryBudgetModel).filter(CategoryBudgetModel.budget_id==budget.id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise BudgetError(message="Error deleting budget", code=status.HTTP_400_BAD_REQUEST)
        finally:
            session.close()
            
        return BudgetSuccess(message="Budget deleted successfully", code=status.HTTP_204_NO_CONTENT)