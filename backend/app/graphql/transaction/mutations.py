import strawberry
from uuid import UUID
from .types import *
from ...utils import db
from ...utils.handler import login_required, DatabaseHandler
from strawberry import Info
from typing import Optional
import datetime
from ...models import UserModel,TransactionModel
from ...models.transaction import transaction_type_list
from sqlalchemy import sql
from typing import Union

@strawberry.input
class CreateTransactionInput:
    amount:float
    description:str
    category:str
    date:Optional[datetime.datetime] = None
    type:str
    
@strawberry.input
class DeleteTransactionInput:
    id:UUID

@strawberry.input
class UpdateTransactionInput:
    id:UUID 
    amount:Optional[float] = None
    description:Optional[str] = None
    category:Optional[str] = None
    transaction_date:Optional[datetime.datetime] =None
    

def validate_create_input(input:CreateTransactionInput):
    errors = []
    if input.type not in transaction_type_list:
        errors.append("Type must be 'income', 'expense' or 'other' ")
    return errors

@strawberry.type
class TransactionMutation:
    
    @strawberry.mutation
    @login_required
    def createTransaction(self, input:CreateTransactionInput, info:Info) ->TransactionType:
        session = db.get_session()
        user:UserModel = info.context.get("user")
        
        #Validate input
        errors = validate_create_input(input)
        if errors:
            # return CreateTransactionResponse(statusCode=400, errors=errors)
            raise TransactionOperationError(code=status.HTTP_400_BAD_REQUEST, message="Invalid input")
        
        new_transaction = TransactionModel(amount = input.amount, description = input.description, category = input.category, date = input.date, user_id = user.id, type=input.type)
        DatabaseHandler.create_new_transaction(session=session, transaction_doc=new_transaction)
        
        
        return TransactionType(new_transaction)
    
    @strawberry.mutation
    @login_required
    def deleteTransaction(self, input: DeleteTransactionInput, info:Info) ->TransactionOperationSuccess:
        session = db.get_session()
        user:UserModel = info.context.get("user")
        existing_transaction = DatabaseHandler.get_transaction_by_id(session, input.id)
        
        if user.id != existing_transaction.user_id:
            # return DeleteTransactionResponse(error="Unauthorized", statusCode=401)
            raise TransactionOperationError(message="Unauthorized", code = status.HTTP_401_UNAUTHORIZED, detail="You are not the person who creates this transaction")
        
        if not existing_transaction or existing_transaction.deleted_at:
            # return DeleteTransactionResponse(error="This transaction does not exist", statusCode=404)
            raise TransactionOperationError(message="This transaction does not exist", code = status.HTTP_404_NOT_FOUND)
        
        existing_transaction.deleted_at = sql.func.now()
        session.commit()
        
        return TransactionOperationSuccess(message="Deleted transaction successfully", statusCode=200)
    
    @strawberry.mutation
    @login_required
    def updateTransaction(self,input:UpdateTransactionInput, info:Info)->TransactionOperationSuccess:
        session = db.get_session()
        user:UserModel = info.context.get("user")
        existing_transaction = DatabaseHandler.get_transaction_by_id(session, input.id)
        
        
        if user.id != existing_transaction.user_id:
            raise TransactionOperationError(message="Unauthorized", code = status.HTTP_401_UNAUTHORIZED, detail="You are not the person who creates this transaction")
        
        if not existing_transaction or existing_transaction.deleted_at:
            raise TransactionOperationError(message="This transaction does not exist", code = status.HTTP_404_NOT_FOUND)
        
        if existing_transaction.amount:
            existing_transaction.amount = input.amount
        if existing_transaction.category:
            existing_transaction.category = input.category
        if existing_transaction.description:
            existing_transaction.description = input.description
        if existing_transaction.transaction_date:
            existing_transaction.transaction_date = input.transaction_date
            
        existing_transaction.updated_at = sql.func.now()
        session.commit()
        return TransactionOperationSuccess(statusCode=200, data="Updated transaction Successfully")
        
        
        