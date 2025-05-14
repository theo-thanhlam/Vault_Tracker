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
from ..baseType import BaseInput

@strawberry.input
class CreateTransactionInput(BaseInput):
    amount:float
    description:str
    category:str
    date:Optional[datetime.datetime] = None
    type:str
    
@strawberry.input
class DeleteTransactionInput(BaseInput):
    id:UUID

@strawberry.input
class UpdateTransactionInput(BaseInput):
    id:UUID 
    amount:Optional[float] = None
    description:Optional[str] = None
    category:Optional[str] = None
    date:Optional[datetime.datetime] =None
    type:Optional[str] = None
    

def validate_create_input(input:CreateTransactionInput):
    errors = []
    if input.type not in transaction_type_list:
        errors.append("Type must be 'income', 'expense' or 'other' ")
    return errors

def update_existing_transaction(existing_transaction:TransactionModel,input:UpdateTransactionInput)->TransactionModel:
    parsed_input = input.parse()
    
    for k,v in parsed_input.items():
        if v is not None:
            setattr(existing_transaction, k, v)
    existing_transaction.updated_at = sql.func.now()
    return existing_transaction

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
        parsed_input = input.parse()
        new_transaction = TransactionModel(user_id = user.id, **parsed_input)
        DatabaseHandler.create_new_transaction(session=session, transaction_doc=new_transaction)
        
        return TransactionType(**new_transaction.to_dict())
    
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
    def updateTransaction(self,input:UpdateTransactionInput, info:Info)->TransactionType:
        session = db.get_session()
        user:UserModel = info.context.get("user")
        existing_transaction = DatabaseHandler.get_transaction_by_id(session, input.id)
        
        
        if user.id != existing_transaction.user_id:
            raise TransactionOperationError(message="Unauthorized", code = status.HTTP_401_UNAUTHORIZED, detail="You are not the person who creates this transaction")
        
        if not existing_transaction or existing_transaction.deleted_at:
            raise TransactionOperationError(message="Not found", code = status.HTTP_404_NOT_FOUND, detail="This transaction does not exist")
        
        
        existing_transaction = update_existing_transaction(existing_transaction, input)
        session.commit()
        return TransactionType(**existing_transaction.to_dict())
        
        
        