import strawberry
from uuid import UUID
from .types import *
from ...utils import db
from ...models import UserModel
from ...utils.handler import DatabaseHandler
from fastapi import HTTPException,status
from strawberry import Info


@strawberry.input
class GetTransactionInput:
    transaction_id:UUID
    

@strawberry.type
class TransactionQuery:
    @strawberry.field
    def getTransactions(self, info:Info) -> GetAllTransactionsResponse:
        user = info.context.get("user")
        session = db.get_session()
        user_transactions = DatabaseHandler.get_all_transactions_by_user_id(session=session, user_id=user.id)
        return GetAllTransactionsResponse(transactions=user_transactions, message=f"Here are all {user.firstName} {user.lastName}'s transactions", code=status.HTTP_200_OK)
    @strawberry.field
    def getTransaction(self, input:GetTransactionInput, info:Info) -> TransactionType:
        
        session = db.get_session()
        user_transactions = DatabaseHandler.get_transaction_by_id(session=session, id=input.transaction_id)
        return TransactionType(user_transactions)
        