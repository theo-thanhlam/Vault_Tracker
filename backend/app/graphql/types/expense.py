from .base import BaseType, strawberry
import datetime


@strawberry.type
class ExpenseType(BaseType):
    
    amount:float
    description:str | None
    category:str
    expense_date:datetime.date