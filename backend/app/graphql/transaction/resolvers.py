import strawberry
from uuid import UUID
from .types import TransactionType, GetTransactionsResponse
from ...utils import db
from ...models import UserModel
from ...utils.handler import DatabaseHandler
from fastapi import HTTPException
from strawberry import Info


@strawberry.input
class GetTransactionInput:
    transaction_id:UUID
    

@strawberry.type
class TransactionQuery:

    
    @strawberry.field
    def getTransactions(self, info:Info) -> GetTransactionsResponse:
        user = info.context.get("user")
        session = db.get_session()
        user_transactions = DatabaseHandler.get_all_transactions_by_user_id(session=session, user_id=user.id)
        return GetTransactionsResponse(transactions=user_transactions)
        