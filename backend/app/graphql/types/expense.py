from .base import BaseType, strawberry
import datetime


@strawberry.type
class ExpenseType(BaseType):
    
    amount:float
    description:str
    category:str
    expense_date:datetime.date