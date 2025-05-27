import strawberry
from uuid import UUID
from .types import *
from ...utils import db
from ...utils.handler import login_required, DatabaseHandler
from strawberry import Info
from typing import Optional
import datetime
from ...models.core import TransactionTypeEnum, UserModel,TransactionModel,CategoryModel
from sqlalchemy import sql
from typing import Union
from ..base.types import BaseInput
from fastapi import status
from ..base.mutations import BaseAuthenticatedMutation

@strawberry.input
class CreateTransactionInput(BaseInput):
    amount:float
    description:str
    category_id:UUID
    date:Optional[datetime.datetime] = None
    # type:TransactionTypeEnum
    
@strawberry.input
class DeleteTransactionInput(BaseInput):
    id:UUID

@strawberry.input
class UpdateTransactionInput(BaseInput):
    id:UUID 
    amount:Optional[float] = None
    description:Optional[str] = None
    category_id:Optional[UUID] = None
    date:Optional[datetime.datetime] =None
    
    # type:Optional[str] = None
    



def update_existing_transaction(existing_transaction:TransactionModel,input:UpdateTransactionInput)->TransactionModel:
    parsed_input = input.to_dict()
    
    for k,v in parsed_input.items():
        if v is not None:
            setattr(existing_transaction, k, v)
    existing_transaction.updated_at = sql.func.now()
    return existing_transaction

# @strawberry.type
# class TransactionMutation:
    
#     @strawberry.mutation
#     def create(self, input:CreateTransactionInput, info:Info) ->TransactionSuccess:
#         session = db.get_session()
#         user:UserModel = info.context.get("user")

#         existing_category : CategoryModel = session.get(CategoryModel,input.category_id)
#         if not existing_category:
#             raise TransactionError(code=status.HTTP_404_NOT_FOUND, message="Not Found", detail="This category does not exist, please choose different category or create a new one")
        
#         parsed_input = input.to_dict()
#         new_transaction = TransactionModel(user_id = user.id, **parsed_input)
#         DatabaseHandler.create_new_transaction(session=session, transaction_doc=new_transaction)
#         success_data = {
#             "code":status.HTTP_201_CREATED, 
#             "message":"Created new transaction successfully",
#             "transaction":TransactionType(**new_transaction.to_dict())
#         }
        
#         # return TransactionType(**new_transaction.to_dict())
#         return TransactionSuccess( **success_data)
    
#     @strawberry.mutation
#     def delete(self, input: DeleteTransactionInput, info:Info) ->TransactionSuccess:
#         session = db.get_session()
#         user:UserModel = info.context.get("user")
#         existing_transaction = DatabaseHandler.get_transaction_by_id(session, input.id)
        
#         if user.id != existing_transaction.user_id:
#             raise TransactionError(message="Unauthorized", code = status.HTTP_401_UNAUTHORIZED, detail="You are not the person who creates this transaction")
        
#         if not existing_transaction or existing_transaction.deleted_at:
#             raise TransactionError(message="This transaction does not exist", code = status.HTTP_404_NOT_FOUND)
        
#         existing_transaction.deleted_at = sql.func.now()
#         session.commit()
        
#         return TransactionSuccess(message="Deleted transaction successfully", code=200)
    
#     @strawberry.mutation
#     def update(self,input:UpdateTransactionInput, info:Info)->TransactionSuccess:
#         session = db.get_session()
#         user:UserModel = info.context.get("user")
#         existing_transaction = DatabaseHandler.get_transaction_by_id(session, input.id)
        
#         if not existing_transaction or existing_transaction.deleted_at:
#             raise TransactionError(message="Not found", code = status.HTTP_404_NOT_FOUND, detail="This transaction does not exist")
#         if user.id != existing_transaction.user_id:
#             raise TransactionError(message="Unauthorized", code = status.HTTP_401_UNAUTHORIZED, detail="You are not the person who creates this transaction")
        
        
#         existing_category : CategoryModel = session.get(CategoryModel,
#                                                         input.category_id if input.category_id else existing_transaction.category_id
#                                                         ) 
#         if not existing_category:
#             raise TransactionError(code=status.HTTP_404_NOT_FOUND, message="Not Found", detail="This category does not exist, please choose different category or create a new one")
        
#         existing_transaction = update_existing_transaction(existing_transaction, input)
#         session.commit()
        
        
#         success_data = {
#             "code":status.HTTP_200_OK,
#             "message":"Updated transaction successfully",
#             "transaction":TransactionType(**existing_transaction.to_dict())
#         }
#         return TransactionSuccess(**success_data)
        
@strawberry.type
class TransactionMutation(BaseAuthenticatedMutation):
    """
    Handles all transaction-related mutations including create, update, and delete.

    Inherits:
        BaseAuthenticatedMutation: A generic mutation handler with auth checks and CRUD logic.

    Class Attributes:
        model: The SQLAlchemy model associated with this mutation (`TransactionModel`).
        success_type: The GraphQL success response type (`TransactionSuccess`).
        type: The return type for individual transaction instances (`TransactionType`).

    Mutations:
        create: Adds a new transaction.
        update: Updates an existing transaction.
        delete: Performs a soft delete on an existing transaction.
    """
    model = TransactionModel
    success_type = TransactionSuccess
    type = TransactionType
    
    
    @strawberry.mutation
    def create(self, input:CreateTransactionInput, info:strawberry.Info) -> TransactionSuccess:
        """
        Creates a new transaction.

        Args:
            input (CreateTransactionInput): Data required to create the transaction.
            info (strawberry.Info): GraphQL context containing the authenticated user.

        Returns:
            TransactionSuccess: Response indicating success and returning the created transaction.
        """
        return super().create(input, info)
    
    @strawberry.mutation
    def update(self, input:UpdateTransactionInput, info:strawberry.Info) -> TransactionSuccess:
        """
        Updates an existing transaction.

        Args:
            input (UpdateTransactionInput): Data for the transaction to be updated (must include `id`).
            info (strawberry.Info): GraphQL context.

        Returns:
            TransactionSuccess: Response with the updated transaction data.
        """
        return super().update(input, info)
    
    @strawberry.mutation
    def delete(self, input:DeleteTransactionInput, info:strawberry.Info) -> TransactionSuccess:
        """
        Performs a soft delete on the specified transaction.

        Args:
            input (DeleteTransactionInput): Input containing the `id` of the transaction to be deleted.
            info (strawberry.Info): GraphQL context.

        Returns:
            TransactionSuccess: Response confirming the deletion.
        """
        return super().delete(input, info)
        