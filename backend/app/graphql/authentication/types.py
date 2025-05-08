from uuid import UUID
from ..expense.types import ExpenseType
from ..baseType import *

from typing import List,Generic, TypeVar
import strawberry
from datetime import datetime
from strawberry.exceptions import StrawberryException
from typing import Optional

T = TypeVar("T")


@strawberry.type
class UserType(BaseType):

    firstName:str 
    lastName:str
    email:str
    expenses: List[ExpenseType]

@strawberry.type(description="Generic response wrapper")
class AuthBaseSuccess:
    token: Optional[str] = strawberry.field(description="Authentication Token")

@strawberry.type(description="Generic response wrapper")
class AuthBaseError:
    message: Optional[str] = strawberry.field(description="Error message")
    
@strawberry.type(description="Successful registration response")
class RegisterUserSuccess(AuthBaseSuccess):
    created_at: Optional[datetime] = strawberry.field(description="Datetime the user account was created")

@strawberry.type
class RegisterUserError(AuthBaseError):
    pass

@strawberry.type(description="Response wrapper for user registration.")
class RegisterUserResponse(BaseResponse[RegisterUserSuccess, RegisterUserError]):
    data: Optional[RegisterUserSuccess] = strawberry.field(default=None, description="Registration result on success")
    error: Optional[RegisterUserError] = strawberry.field(default=None, description="List of errors, if any")
    statusCode:int = strawberry.field(description="HTTP code")
    
@strawberry.type(description="Successful registration response")
class LoginUserSuccess(AuthBaseSuccess):
    pass

@strawberry.type
class LoginUserError(AuthBaseError):
    pass

@strawberry.type(description="Response wrapper for user login")
class LoginUserResponse(BaseResponse[LoginUserSuccess,LoginUserError]):
    data: Optional[LoginUserSuccess] = strawberry.field(default=None, description="Registration result on success")
    error: Optional[LoginUserError] = strawberry.field(default=None, description="List of errors, if any")
    statusCode:int = strawberry.field(description="HTTP code")
    
    
@strawberry.type(description="")
class GetCurrentUserSuccess(UserType):
    pass

@strawberry.type
class GetCurrentUserError(AuthBaseError):
    pass   

@strawberry.type
class GetCurrentUserResponse(BaseResponse[GetCurrentUserSuccess,GetCurrentUserError]):
    data: Optional[GetCurrentUserSuccess] = strawberry.field(default=None)
    error: Optional[GetCurrentUserError] = strawberry.field(default=None, description="List of errors, if any")
    statusCode:int = strawberry.field(description="HTTP code")