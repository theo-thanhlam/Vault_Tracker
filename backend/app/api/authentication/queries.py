import strawberry
from uuid import UUID
from strawberry.types import Info
from .types import *
from ...models.user import UserModel
from ...utils.handler import login_required


@strawberry.input
class UserQueryInput:
    id:UUID

@strawberry.type(description="Handle authentication queries")
class AuthQuery:
    
    @strawberry.field(description="[Login required] Return user information from the context")
    @login_required
    def getCurrentUser(self, info:Info) -> GetUserSuccess:
        
        user:UserModel = info.context.get("user")
        user_dict = {k:v for k,v in user.to_dict().items() if k != 'password'}
        
        
        return AuthSucess(code=200, message="Get user successfully", values= UserType(**user_dict))
        
        