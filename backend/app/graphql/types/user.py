
from uuid import UUID
from .base import BaseType, strawberry
from typing import List
from .transaction import TransactionType

@strawberry.type
class UserType(BaseType):
    firstName:str 
    lastName:str
    email:str
    password:str
    transactions:List[TransactionType]
    