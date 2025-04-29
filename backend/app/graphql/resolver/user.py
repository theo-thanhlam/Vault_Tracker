import strawberry
from uuid import UUID
from ..types import UserType
from ...utils import db
from ...models import UserModel
from fastapi import HTTPException

@strawberry.type
class UserQuery:
    @strawberry.field
    def get_user(self, id:UUID) ->UserType:
        engine = db.get_engine()
        with db.Session(engine) as session:
            user = session.get(UserModel, id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return UserType(id=user.id, firstName = user.firstName, lastName = user.lastName, transactions = user.transactions)