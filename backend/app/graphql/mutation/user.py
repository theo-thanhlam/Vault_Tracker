import strawberry
from uuid import UUID
from ..types import UserType
from ...utils import db
from ...models import UserModel
from fastapi import HTTPException

@strawberry.type
class UserMutation:
    @strawberry.mutation
    def create_user(self, firstName:str, lastName:str, email:str, password:str) ->UserType:
        engine = db.get_engine()
        with db.Session(engine) as session:
            new_user = UserModel(firstName=firstName, lastName=lastName, email=email, password=password)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return UserType(id = new_user.id, firstName=new_user.firstName, lastName=new_user.lastName, email=new_user.email, transactions=[])
      