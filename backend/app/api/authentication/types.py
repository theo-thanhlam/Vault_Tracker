
from ..transaction.types import TransactionType
from ..base.types import *

from typing import List
import strawberry
from ...models.user import UserRoleEnum
from typing import Optional
from strawberry.scalars import JSON


@strawberry.type
class UserType(BaseType):
    firstName:Optional[str] = None 
    lastName:Optional[str] = None
    email:str
    role:UserRoleEnum
    email_verified:bool
    auth_provider_id:Optional[str] = None 
    

@strawberry.type
class AuthSucess(BaseSuccess[JSON]):
    token: Optional[str] = strawberry.field(description="Authentication token", default=None)
    pass
    


class AuthError(BaseError):
    pass

@strawberry.type
class GetUserSuccess(BaseSuccess[UserType]):
    pass
    

