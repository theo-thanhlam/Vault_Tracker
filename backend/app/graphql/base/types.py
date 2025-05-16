import strawberry
from uuid import UUID
from datetime import datetime


from strawberry.exceptions import StrawberryGraphQLError
from fastapi import status
from typing import Any, Optional, Type, TypeVar, Generic









@strawberry.type
class BaseType:
    id:UUID 
    created_at:datetime 
    updated_at:datetime |None = None
    deleted_at:datetime |None = None

@strawberry.type
class BaseError(StrawberryGraphQLError):
    message:str
    code:status
    detail:str = None
    def __init__(self, message:str, code:status, detail:str=None):
        self.message=message
        self.code = code
        self.detail = detail
        super().__init__(
            
            message=self.message, 
            extensions={
                "statusCode":self.code,
                "detail":self.detail
            }
        )
        
TResponse = TypeVar("TResponse", bound=BaseType)

@strawberry.interface
class BaseResponse:
    message: str = strawberry.field( description="Success message")
    code: int = strawberry.field(description="HTTP status code")
    
    
@strawberry.type
class BaseSuccess(BaseResponse):
    # values:TResponse = strawberry.field(default=None, description="Return values")
    pass
    
    
    

@strawberry.input
class BaseInput:
    def to_dict(self)->dict[str, Any]:
        return strawberry.asdict(self)
    
