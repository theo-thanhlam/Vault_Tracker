import strawberry
from uuid import UUID
from .types import *
from ...utils import db
from ...utils.handler import login_required, DatabaseHandler
from strawberry import Info
from typing import Optional
import datetime
from ...models import UserModel,ExpenseModel
from sqlalchemy import sql


@strawberry.input
class CreateExpenseInput:
    amount:float
    description:str
    category:str
    expense_date:Optional[datetime.datetime] 
    
@strawberry.input
class DeleteExpenseInput:
    id:UUID

@strawberry.input
class UpdateExpenseInput:
    id:UUID 
    amount:Optional[float] = None
    description:Optional[str] = None
    category:Optional[str] = None
    expense_date:Optional[datetime.datetime] =None

@strawberry.type
class ExpenseMutation:
    
    @strawberry.mutation
    @login_required
    def createExpense(self, input:CreateExpenseInput, info:Info) ->CreateExpenseResponse:
        session = db.get_session()
        user:UserModel = info.context.get("user")
        
        try:
            new_expense = ExpenseModel(amount = input.amount, description = input.description, category = input.category, expense_date = input.expense_date, user_id = user.id)
            DatabaseHandler.create_new_expense(session=session, expense_doc=new_expense)
        except Exception as e:
            return CreateExpenseResponse(statusCode=500, error="Error when creating new expense")
        
        return CreateExpenseResponse(statusCode=200, data="Created new expense Successfully")
    
    @strawberry.mutation
    @login_required
    def deleteExpense(self, input: DeleteExpenseInput, info:Info) ->DeleteExpenseResponse:
        session = db.get_session()
        user:UserModel = info.context.get("user")
        existing_expense = DatabaseHandler.get_expense_by_id(session, input.id)
        
        if user.id != existing_expense.user_id:
            return DeleteExpenseResponse(error="Unauthorized", statusCode=401)
        
        if not existing_expense or existing_expense.deleted_at:
            return DeleteExpenseResponse(error="This expense does not exist", statusCode=404)
        
        existing_expense.deleted_at = sql.func.now()
        session.commit()
        
        return DeleteExpenseResponse(data="Deleted expense successfully", statusCode=200)
    
    @strawberry.mutation
    @login_required
    def updateExpense(self,input:UpdateExpenseInput, info:Info)->UpdateExpenseResponse:
        session = db.get_session()
        user:UserModel = info.context.get("user")
        existing_expense = DatabaseHandler.get_expense_by_id(session, input.id)
        
        
        if user.id != existing_expense.user_id:
            return UpdateExpenseResponse(error="Unauthorized", statusCode=401)
        
        if not existing_expense or existing_expense.deleted_at:
            return UpdateExpenseResponse(error="This expense does not exist", statusCode=404)
        
        if existing_expense.amount:
            existing_expense.amount = input.amount
        if existing_expense.category:
            existing_expense.category = input.category
        if existing_expense.description:
            existing_expense.description = input.description
        if existing_expense.expense_date:
            existing_expense.expense_date = input.expense_date
            
        existing_expense.updated_at = sql.func.now()
        session.commit()
        return UpdateExpenseResponse(statusCode=200, data="Updated expense Successfully")
        
        
        