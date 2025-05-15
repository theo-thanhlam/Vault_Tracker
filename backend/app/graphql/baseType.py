import strawberry
from uuid import UUID
from datetime import datetime


from strawberry.exceptions import StrawberryGraphQLError
from fastapi import status
from typing import Any
from strawberry_sqlalchemy_mapper import StrawberrySQLAlchemyMapper





@strawberry.type
class BaseType:
    id:UUID 
    created_at:datetime 
    updated_at:datetime |None = None
    deleted_at:datetime |None = None

@strawberry.interface
class BaseError(StrawberryGraphQLError):
    def __init__(self, message:str, code:status, detail:str=None):
        super().__init__(
            
            message=message, 
            extensions={
                "statusCode":code,
                "detail":detail
            }
        )
@strawberry.interface
class BaseResponse:
    message: str = strawberry.field( description="Success message")
    code: int = strawberry.field(description="HTTP status code")
    
@strawberry.interface
class BaseSuccess(BaseResponse):
    pass

@strawberry.input
class BaseInput:
    def to_dict(self)->dict[str, Any]:
        return strawberry.asdict(self)
    
strawberry_sqlalchemy_mapper = StrawberrySQLAlchemyMapper()