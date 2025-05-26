import strawberry
from uuid import UUID
from datetime import datetime

from strawberry.scalars import JSON
from strawberry.exceptions import StrawberryGraphQLError
from fastapi import status
from typing import Any, Optional, Type, TypeVar, Generic, Dict


@strawberry.type
class BaseType:
    """
    Custom error class for handling GraphQL API errors.

    Attributes:
        message (str): Error message.
        code (status): HTTP status code representing the error.
        detail (Optional[str]): Additional detail for the error (optional).
    """
    id:UUID 
    created_at:datetime 
    updated_at:datetime |None = None
    deleted_at:datetime |None = None

@strawberry.type
class BaseError(StrawberryGraphQLError):
    """
    Custom error class for handling GraphQL API errors.

    Attributes:
        message (str): Error message.
        code (status): HTTP status code representing the error.
        detail (Optional[str]): Additional detail for the error (optional).
    """
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
        


@strawberry.interface
class BaseResponse:
    """
    Common interface for all responses, both success and error types.

    Fields:
        message (str): Human-readable message describing the result.
        code (int): HTTP status code for the operation.
    """
    message: str = strawberry.field( description="Success message")
    code: int = strawberry.field(description="HTTP status code")
    
   
TResponse = TypeVar("TResponse", bound=BaseType) 
@strawberry.type
class BaseSuccess(BaseResponse,Generic[TResponse]):
    """
    Generic success response type.

    Inherits:
        BaseResponse: Includes message and code.

    Fields:
        values (Optional[TResponse]): The payload object (can be `None` if no data is returned).
    """
    # values:Dict[str,Any] = strawberry.field(default_factory=dict, description="Return values")
    values:Optional[TResponse] = strawberry.field(default=None, description="Return success values")


    
    
    

@strawberry.input
class BaseInput:
    """
    Base input type for mutations. Meant to be extended by create/update/delete input types.

    Methods:
        to_dict(): Converts the Strawberry input object into a dictionary.
    """
    def to_dict(self)->dict[str, Any]:
        return strawberry.asdict(self)
    
