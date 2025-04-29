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
    # password:str
    expenses: List[ExpenseType]