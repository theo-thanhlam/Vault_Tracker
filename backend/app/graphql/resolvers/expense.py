import strawberry
from uuid import UUID
from ..types import ExpenseType
from ...utils import db
from ...models import UserModel
from fastapi import HTTPException
from strawberry import Info

@strawberry.type
class ExpenseQuery:
    @strawberry.field
    def get_expense(self,id:UUID, info:Info) -> ExpenseType:
        session =db.get_db()
        
        
        
       
       
    
    