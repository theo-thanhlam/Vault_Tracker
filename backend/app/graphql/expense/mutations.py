import strawberry
from uuid import UUID
from .types import ExpenseType
from ...utils import db
from ...models import UserModel
from fastapi import HTTPException


@strawberry.input
class ExpenseInput:
    pass

@strawberry.type
class ExpenseMutation:
     def createExpense(self, input:ExpenseInput) ->ExpenseType:
        session = db.get_session()
        pass