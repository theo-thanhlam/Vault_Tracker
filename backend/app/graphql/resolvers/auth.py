import strawberry
from uuid import UUID
from ..types import UserType
from ...utils import db,auth
from ...models import UserModel
from fastapi import HTTPException
from datetime import datetime
from strawberry.types import Info
from ..types import *


@strawberry.input
class UserQueryInput:
    id:UUID

@strawberry.type
class UserQuery:
    
    
    @strawberry.field
    def getCurrentUser(self, info:Info) -> GetCurrentUserResponse:
        
        user = info.context.get("user")
        if not user:
            return GetCurrentUserResponse(error=GetCurrentUserError(message="Not Authenticated"), statusCode=401)
        user_doc = UserType(id=user.id, firstName = user.firstName, lastName = user.lastName, expenses = user.expenses, created_at=user.created_at, email=user.email)
        return GetCurrentUserResponse(data=user_doc,statusCode=200)
        