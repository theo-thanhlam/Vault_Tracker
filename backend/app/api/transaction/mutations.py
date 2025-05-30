import strawberry
from uuid import UUID
from .types import *
from ...utils import db
from ...utils.handler import login_required, DatabaseHandler
from strawberry import Info
from typing import Optional, List
import datetime
from ...models.core import TransactionTypeEnum, UserModel,TransactionModel,CategoryModel,BudgetModel,GoalModel      
from ...models.associative import TransactionCategoryModel, TransactionGoalModel, TransactionBudgetModel
from sqlalchemy import sql
from typing import Union
from ..base.types import BaseInput
from fastapi import status
from ..base.mutations import BaseAuthenticatedMutation
from .validator import TransactionMutationValidator

@strawberry.input
class CategoryAllocationInput(BaseInput):
    category_id:UUID = strawberry.field(description="The ID of the category to allocate to the transaction")
    amount:float
    
@strawberry.input
class GoalAllocationInput(BaseInput):
    goal_id:UUID
    amount:float

@strawberry.input
class BudgetAllocationInput(BaseInput):
    budget_id:UUID
    amount:float


@strawberry.input
class CreateTransactionInput(BaseInput):
    amount:float
    description:str
    # category_id:UUID
    date:Optional[datetime.datetime] = None
    # type:TransactionTypeEnum
    categories:List[CategoryAllocationInput]
    goals:Optional[List[GoalAllocationInput]] = None
    budgets:Optional[List[BudgetAllocationInput]] = None
    
@strawberry.input
class DeleteTransactionInput(BaseInput):
    id:UUID

@strawberry.input
class UpdateTransactionInput(BaseInput):
    id:UUID 
    amount:Optional[float] = None
    description:Optional[str] = None
    date:Optional[datetime.datetime] = None
    categories:Optional[List[CategoryAllocationInput]] = None
    goals:Optional[List[GoalAllocationInput]] = None
    budgets:Optional[List[BudgetAllocationInput]] = None
    
    # type:Optional[str] = None
    



def update_existing_transaction(existing_transaction:TransactionModel,input:UpdateTransactionInput)->TransactionModel:
    parsed_input = input.to_dict()
    
    for k,v in parsed_input.items():
        if v is not None:
            setattr(existing_transaction, k, v)
    existing_transaction.updated_at = sql.func.now()
    return existing_transaction

@strawberry.type
class TransactionMutation:
    
    
    @strawberry.mutation
    @login_required
    def create(self, input:CreateTransactionInput, info:Info) -> TransactionSuccess:
        session = db.get_session()
        user:UserModel = info.context.get("user")
        validator = TransactionMutationValidator(session=session, input=input, user=user)
        try:
            category_allocations, goal_allocations, budget_allocations = validator.validate_create_input()
            parsed_input = input.to_dict()
            new_transaction = TransactionModel(user_id = user.id, amount=parsed_input["amount"], description=parsed_input["description"], date=parsed_input["date"])
            DatabaseHandler.create_new_transaction(session=session, transaction_doc=new_transaction)
            
            for category_allocation in parsed_input["category_allocations"]:
                new_transaction_category = TransactionCategoryModel(transaction_id=new_transaction.id, category_id=category_allocation["category_id"], amount=category_allocation["amount"])
                session.add(new_transaction_category)

            for goal_allocation in parsed_input["goal_allocations"]:
                new_transaction_goal = TransactionGoalModel(transaction_id=new_transaction.id, goal_id=goal_allocation["goal_id"], amount=goal_allocation["amount"])
                session.add(new_transaction_goal)
                
            for budget_allocation in parsed_input["budget_allocations"]:
                new_transaction_budget = TransactionBudgetModel(transaction_id=new_transaction.id, budget_id=budget_allocation["budget_id"], amount=budget_allocation["amount"])
                session.add(new_transaction_budget)
                
            session.commit()
            success_data = {
                "code":status.HTTP_201_CREATED,
                "message":"Transaction created successfully",
                "values":TransactionType(**new_transaction.to_dict(), categories=category_allocations, goals=goal_allocations, budgets=budget_allocations)
            }
            return TransactionSuccess(**success_data)
                
        except TransactionError as e:
            raise TransactionError(message=e.message, code=e.code)
        except Exception as e:
            raise TransactionError(message="Failed to create transaction", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @strawberry.mutation
    @login_required
    def update(self, input:UpdateTransactionInput, info:Info) -> TransactionSuccess:
        session = db.get_session()
        user:UserModel = info.context.get("user")
        validator = TransactionMutationValidator(session=session, input=input, user=user)
        
        try:
            # Validate input and get existing transaction
            category_allocations, goal_allocations, budget_allocations = validator.validate_update_input()
            existing_transaction = DatabaseHandler.get_transaction_by_id(session, input.id)
            
            if not existing_transaction or existing_transaction.deleted_at:
                raise TransactionError(message="Transaction not found", code=status.HTTP_404_NOT_FOUND)
            
            if user.id != existing_transaction.user_id:
                raise TransactionError(message="Unauthorized", code=status.HTTP_401_UNAUTHORIZED)
            
            # Update basic transaction fields
            parsed_input = input.to_dict()
            existing_transaction = update_existing_transaction(existing_transaction, input)
            
            # Delete existing allocations
            session.query(TransactionCategoryModel).filter_by(transaction_id=existing_transaction.id).delete()
            session.query(TransactionGoalModel).filter_by(transaction_id=existing_transaction.id).delete()
            session.query(TransactionBudgetModel).filter_by(transaction_id=existing_transaction.id).delete()
            
            # Add new allocations
            if parsed_input.get("category_allocations"):
                for allocation in parsed_input["category_allocations"]:
                    new_allocation = TransactionCategoryModel(
                        transaction_id=existing_transaction.id,
                        category_id=allocation["category_id"],
                        amount=allocation["amount"]
                    )
                    session.add(new_allocation)
            
            if parsed_input.get("goal_allocations"):
                for allocation in parsed_input["goal_allocations"]:
                    new_allocation = TransactionGoalModel(
                        transaction_id=existing_transaction.id,
                        goal_id=allocation["goal_id"],
                        amount=allocation["amount"]
                    )
                    session.add(new_allocation)
            
            if parsed_input.get("budget_allocations"):
                for allocation in parsed_input["budget_allocations"]:
                    new_allocation = TransactionBudgetModel(
                        transaction_id=existing_transaction.id,
                        budget_id=allocation["budget_id"],
                        amount=allocation["amount"]
                    )
                    session.add(new_allocation)
            
            session.commit()
            
            return TransactionSuccess(
                code=status.HTTP_200_OK,
                message="Transaction updated successfully",
                values=TransactionType(
                    **existing_transaction.to_dict(),
                    categories=category_allocations,
                    goals=goal_allocations,
                    budgets=budget_allocations
                )
            )
            
        except TransactionError as e:
            session.rollback()
            raise e
        except Exception as e:
            session.rollback()
            raise TransactionError(
                message="Failed to update transaction",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        finally:
            session.close()
        
    @strawberry.mutation
    @login_required
    def delete(self, input:DeleteTransactionInput, info:Info) -> TransactionSuccess:
        session = db.get_session()
        user:UserModel = info.context.get("user")
        
        try:
            # Get and validate transaction
            existing_transaction = DatabaseHandler.get_transaction_by_id(session, input.id)
            
            if not existing_transaction:
                raise TransactionError(message="Transaction not found", code=status.HTTP_404_NOT_FOUND)
            
            if existing_transaction.deleted_at:
                raise TransactionError(message="Transaction already deleted", code=status.HTTP_400_BAD_REQUEST)
            
            if user.id != existing_transaction.user_id:
                raise TransactionError(message="Unauthorized", code=status.HTTP_401_UNAUTHORIZED)
            
            # Soft delete the transaction
            existing_transaction.deleted_at = sql.func.now()
            
            # Delete associated allocations
            session.query(TransactionCategoryModel).filter_by(transaction_id=existing_transaction.id).delete()
            session.query(TransactionGoalModel).filter_by(transaction_id=existing_transaction.id).delete()
            session.query(TransactionBudgetModel).filter_by(transaction_id=existing_transaction.id).delete()
            
            session.commit()
            
            return TransactionSuccess(
                code=status.HTTP_204_NO_CONTENT,
                message="Transaction deleted successfully",
                values=None
            )
            
        except TransactionError as e:
            session.rollback()
            raise e
        except Exception as e:
            session.rollback()
            raise TransactionError(
                message="Failed to delete transaction",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        finally:
            session.close()
        
    def _update_budget_allocations(self, session, transaction_id: UUID, budget_allocations: List[BudgetAllocationInput]) -> None:
        """
        Updates budget allocations for a transaction.
        
        Args:
            session: Database session
            transaction_id: ID of the transaction to update
            budget_allocations: List of new budget allocations
        """
        try:
            # Delete existing budget allocations
            session.query(TransactionBudgetModel).filter_by(transaction_id=transaction_id).delete()
            
            # Add new budget allocations
            if budget_allocations:
                for allocation in budget_allocations:
                    new_allocation = TransactionBudgetModel(
                        transaction_id=transaction_id,
                        budget_id=allocation.budget_id,
                        amount=allocation.amount
                    )
                    session.add(new_allocation)
                    
        except Exception as e:
            session.rollback()
            raise TransactionError(
                message="Failed to update budget allocations",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
