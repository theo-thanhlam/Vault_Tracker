
from ..transaction.types import TransactionType
from ..baseType import *

from typing import List
import strawberry
from strawberry.exceptions import StrawberryGraphQLError
from fastapi import status


@strawberry.type
class UserType(BaseType):

    firstName:str 
    lastName:str
    email:str
    transactions: List[TransactionType]
    
    
@strawberry.type
class AuthSucess(BaseResponse):
    token: str = strawberry.field(description="Authentication token")


class AuthError(BaseError):
    pass
   
    

