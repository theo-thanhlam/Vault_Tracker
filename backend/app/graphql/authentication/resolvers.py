import strawberry
from uuid import UUID
from strawberry.types import Info
from .types import *


@strawberry.input
class UserQueryInput:
    id:UUID

@strawberry.type
class AuthQuery:
    @strawberry.field
    def getCurrentUser(self, info:Info) -> UserType:
        
        user = info.context.get("user")
        
        if not user:
            raise AuthError(message="Unauthorized user", code = status.HTTP_401_UNAUTHORIZED)
        
        return UserType(id=user.id, firstName = user.firstName, lastName = user.lastName, transactions = user.transactions, created_at=user.created_at, email=user.email)
        