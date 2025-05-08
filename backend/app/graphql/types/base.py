import strawberry
from uuid import UUID
from datetime import datetime

from typing import Optional, Generic, TypeVar

# Define generic types
TData = TypeVar("TData")
TError = TypeVar("TErrors")

@strawberry.type
class BaseType:
    id:UUID 
    created_at:datetime 
    updated_at:datetime |None = None
    deleted_at:datetime |None = None
    
@strawberry.type(description="Generic response wrapper")
class BaseResponse(Generic[TData, TError]):
    data: Optional[TData] = strawberry.field(default=None, description="Response payload")
    error: Optional[TError] = strawberry.field(default=None, description="Errors if any")
    statusCode: int = strawberry.field(description="HTTP status code")

@strawberry.type(description="Generic response wrapper")
class AuthBaseSuccess:
    token: Optional[str] = strawberry.field(description="Authentication Token")

@strawberry.type(description="Generic response wrapper")
class AuthBaseError:
    message: Optional[str] = strawberry.field(description="Error message")
