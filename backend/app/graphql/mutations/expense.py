import strawberry
from uuid import UUID
from ..types import UserType
from ...utils import db
from ...models import UserModel
from fastapi import HTTPException


@strawberry.input
class ExpenseInput:
    pass

@strawberry.type
class ExpenseMutation:
     def createExpense(self, input:ExpenseInput) ->UserType:
        session = db.get_session()
        pass