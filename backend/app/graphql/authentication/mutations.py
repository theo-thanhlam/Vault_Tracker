import strawberry

from .types import *
from ...utils import  db
from ...models import UserModel
from ...utils.auth import JWTHandler, EmailHandler, DatabaseHandler, AuthHandler

from fastapi import   Response
from strawberry.types import Info


@strawberry.input(description="Input data required to register a new user")
class RegisterInput:
    firstName: str 
    lastName: str 
    email: str 
    password: str 
    
@strawberry.input(description="Input data required to login")
class LoginInput:
    email: str 
    password: str 

def validate_register_input(input:RegisterInput) -> str|None: 
    errors = []
    if not AuthHandler.check_valid_email(input.email):
        # raise ValueError("Please enter valid email format")
        return "Please enter valid email format"
        
    if not AuthHandler.check_valid_password(input.password):
        return "Please enter a combination of special char, number, uppercase and lowercase characters with at least 12 characters"
        # raise ValueError("Please enter a combination of special char, number, uppercase and lowercase characters with at least 12 characters")
    



@strawberry.type(description="Handles user-related authentication mutations")
class AuthMutation:
    
    @strawberry.mutation( description="Register a new user. Takes user input (first name, last name, email, password), "
                    "creates a new user in the database, and sends a verification email with a token link"
    )
    def register(self, input: RegisterInput) -> RegisterUserResponse:
        session = db.get_session()

        try:
            # Validate input
            validate_error = validate_register_input(input)

            if validate_error:
                return RegisterUserResponse(error=RegisterUserError(message=validate_error) , statusCode=409)
            
            # Check for existing user
            existing_user = DatabaseHandler.get_user_by_email(session, input.email)
            if existing_user:
                return RegisterUserResponse(error=RegisterUserError(message="Existing email"), statusCode=409)

            # Create new user
            hashed_password = AuthHandler.hash_password(input.password)
            new_user = UserModel(
                firstName=input.firstName,
                lastName=input.lastName,
                email=input.email,
                password=hashed_password
            )

            DatabaseHandler.create_new_user(session, new_user)

            # Send email
            token = JWTHandler.create_signup_token(new_user.id)
            EmailHandler.send_verification_email(token=token, user_email=new_user.email)

            success_data = RegisterUserSuccess(
                token=token,
                created_at=new_user.created_at,
            )
            return RegisterUserResponse(data=success_data,statusCode=200)

       

        except Exception as e:
            return RegisterUserResponse(statusCode=500, errors=[RegisterUserError(message="Something went wrong")])
        
    @strawberry.mutation
    def login(self, input:LoginInput, info:Info) -> LoginUserResponse:
        session = db.get_session()
        user = DatabaseHandler.get_user_by_email(session=session, email=input.email)
        
        if not user :
            return LoginUserResponse(error=LoginUserError(message="User does not exist"), statusCode=401)
        
        password_matched = AuthHandler.verify_password(hashed_password=user.password, password=input.password)
        if not password_matched:
            return LoginUserResponse(error=LoginUserError(message="Invalid credential"), statusCode=401)
        
        if not user.is_verified:
            return LoginUserResponse(error=LoginUserError(message="Please verify your email account before continue"), statusCode=401)
        token = JWTHandler.create_login_token(id=user.id)
        success_data = LoginUserSuccess(
            token=token
        )
        
        #Send login cookies to user (HTTP Only)
        response:Response = info.context["response"]
        response.set_cookie("access_token", token, httponly=True)
        
        
        return LoginUserResponse(data=success_data, statusCode=200)
    
    @strawberry.mutation
    def logout(self,info:Info)->None:
        user = info.context.get('user')
        if user:
            info.context['user'] = None
            response: Response = info.context["response"]
            response.delete_cookie("access_token")
        
        
        
        
            

        
        