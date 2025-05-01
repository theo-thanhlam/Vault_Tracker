from uuid import UUID
from ..types import ExpenseType
from .base import BaseType
from typing import List
import strawberry
from datetime import datetime


@strawberry.type
class UserType(BaseType):
    firstName:str 
    lastName:str
    email:str
    expenses: List[ExpenseType]
    
@strawberry.type
class RegisterType:
    token:str
    created_at:datetime 
    