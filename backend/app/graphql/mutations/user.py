import strawberry
from uuid import UUID
from ..types import UserType
from ...utils import db
from ...models import UserModel
from fastapi import HTTPException



@strawberry.input
class UserMutationInput:
    firstName: str
    lastName: str
    email: str
    password: str

@strawberry.type
class UserMutation:
    @strawberry.mutation
    def createUser(self, input:UserMutationInput) ->UserType:
        session = db.get_session()
        
        existing_user = session.query(UserModel).filter_by(email=input.email).first()
        if existing_user:
            raise HTTPException(status_code=409, detail="Existing email")
        
        new_user = UserModel(firstName=input.firstName, lastName=input.lastName, email=input.email, password=input.password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return UserType(
            id = new_user.id, 
            firstName=new_user.firstName, 
            lastName=new_user.lastName, 
            email=new_user.email,
            created_at=new_user.created_at,
            expenses=[]
            )
      