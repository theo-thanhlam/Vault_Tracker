from uuid import UUID
from ..types import ExpenseType
from .base import BaseType
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
    
@strawberry.type(description="Successful registration response")
class RegisterUserSuccess:
    token: Optional[str] = strawberry.field(description="JWT token sent to the user's email")
    created_at: Optional[datetime] = strawberry.field(description="Datetime the user account was created")

     
    
    
@strawberry.type
class RegisterUserError:
    message:Optional[str] = strawberry.field(description="Description of the error")

@strawberry.type(description="Response wrapper for user registration.")
class RegisterUserResponse(Generic[T]):
    data: Optional[RegisterUserSuccess] = strawberry.field(default=None, description="Registration result on success")
    errors: Optional[List[RegisterUserError]] = strawberry.field(default=None, description="List of errors, if any")
    statusCode:int = strawberry.field(description="HTTP code")
    
    
    
