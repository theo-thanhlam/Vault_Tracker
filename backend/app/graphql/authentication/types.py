
from ..transaction.types import TransactionType
from ..base.types import *

from typing import List
import strawberry
from ...models.user import UserRoleEnum
from typing import Optional


@strawberry.type
class UserType(BaseType):
    firstName:str 
    lastName:str
    email:str
    role:UserRoleEnum
    email_verified:bool
    auth_provider_id:Optional[str] = None 
    
    
@strawberry.type
class AuthSucess(BaseSuccess):
    token: str = strawberry.field(description="Authentication token")


class AuthError(BaseError):
    pass
   
    

