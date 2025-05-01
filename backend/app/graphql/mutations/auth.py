import strawberry
from uuid import UUID
from ..types.auth import RegisterType
from ...utils import auth, db
from ...models import UserModel
from fastapi import HTTPException
from ...utils.auth import JWTHandler, EmailHandler



@strawberry.input
class RegisterInput:
    firstName: str
    lastName: str
    email: str
    password: str

@strawberry.type
class AuthMutation:
    
    @strawberry.mutation
    def register(self, input:RegisterInput) ->RegisterType:
        session = db.get_session()
        
        existing_user =  auth.get_user_by_email(session, input.email)
        if existing_user:
            raise HTTPException(status_code=409, detail="Existing email")
        
        hashed_password = auth.hash_password(input.password)
        new_user = UserModel(firstName=input.firstName, lastName=input.lastName, email=input.email, password=hashed_password)
        
        auth.create_new_user(session, new_user)
        
        token = JWTHandler.create_signup_token(new_user.id)
        EmailHandler.send_verification_email(token=token, user_email=new_user.email)
        
        return RegisterType(token=token, created_at=new_user.created_at)
      