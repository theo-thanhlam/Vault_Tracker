import strawberry
from uuid import UUID
from .types import ExpenseType, GetExpensesResponse
from ...utils import db
from ...models import UserModel
from ...utils.handler import DatabaseHandler
from fastapi import HTTPException
from strawberry import Info


@strawberry.input
class GetExpenseInput:
    expense_id:UUID
    

@strawberry.type
class ExpenseQuery:

    
    @strawberry.field
    def getExpenses(self, info:Info) -> GetExpensesResponse:
        user = info.context.get("user")
        session = db.get_session()
        user_expenses = DatabaseHandler.get_all_expenses_by_user_id(session=session, user_id=user.id)
        return GetExpensesResponse(expenses=user_expenses)
        