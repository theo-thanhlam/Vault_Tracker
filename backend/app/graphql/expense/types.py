import strawberry
from ..baseType import BaseType,BaseResponse
from datetime import datetime
from uuid import UUID
from typing import Optional, List

@strawberry.type
class ExpenseType(BaseType):
    amount:float
    description:str
    category:str
    expense_date:datetime 
    user_id:UUID
    
@strawberry.type
class CreateExpenseResponse(BaseResponse[str,str]):
    pass
    
@strawberry.type
class DeleteExpenseResponse(BaseResponse[str,str]):
    pass

@strawberry.type
class UpdateExpenseResponse(BaseResponse[str,str]):
    pass

@strawberry.type
class GetExpensesResponse:
    expenses: List[ExpenseType]