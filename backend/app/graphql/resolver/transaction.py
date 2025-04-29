import strawberry
from uuid import UUID
from ..types import TransactionType
from ...utils import db
from ...models import UserModel
from fastapi import HTTPException

@strawberry.type
class TransactionQuery:
    @strawberry.field
    def get_transaction(self,id:UUID) -> TransactionType:
        engine = db.get_engine()
        with db.Session(engine) as session:
            transaction = session.get(id)
            if not transaction:
                raise HTTPException(status_code = 404 , detail = "Transaction not found")
            return TransactionType(id=transaction.id, amount = transaction.amount)