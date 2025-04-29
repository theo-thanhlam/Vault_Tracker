import strawberry
from uuid import UUID
from ..types import ExpenseType
from ...utils import db
from ...models import UserModel
from fastapi import HTTPException

@strawberry.type
class ExpenseQuery:
    @strawberry.field
    def get_expense(self,id:UUID) -> ExpenseType:
        
        session =db.get_db()
        
        expense = session.get(id)
        if not expense:
            raise HTTPException(status_code = 404 , detail = "Expense not found")
        return ExpenseType(id=expense.id, amount = expense.amount)