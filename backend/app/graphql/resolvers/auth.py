import strawberry
from uuid import UUID
from ..types import UserType
from ...utils import db,auth
from ...models import UserModel
from fastapi import HTTPException
from datetime import datetime


@strawberry.input
class UserQueryInput:
    id:UUID

@strawberry.type
class UserQuery:
    @strawberry.field
    def getUser(self, input:UserQueryInput) ->UserType:
        session = db.get_session()
        user = auth.get_user_by_id(session, input.id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserType(id=user.id, firstName = user.firstName, lastName = user.lastName, expenses = user.expenses, created_at=user.created_at, email=user.email)