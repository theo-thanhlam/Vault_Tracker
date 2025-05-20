import strawberry

from .types import *
from ...utils import  db
from ...models import UserModel,AuthProviderModel, AuthProviderName
from ...utils.handler import *

from fastapi import   Response
from strawberry.types import Info
from strawberry.scalars import JSON



@strawberry.input(description="Input data required to register a new user")
class RegisterInput(BaseInput):
    firstName: str 
    lastName: str 
    email: str 
    password: str 
    
@strawberry.input(description="Input data required to login")
class LoginInput(BaseInput):
    email: str 
    password: str
    
@strawberry.input(description="Google login")
class GoogleLoginInput(BaseInput):
    idToken:str
    
@strawberry.input(description="Verify user email")
class VerifyEmailInput(BaseInput):
    token:str

def validate_register_input(input:RegisterInput) -> str|None: 
    errors = []
    if not AuthHandler.check_valid_email(input.email):
        # raise ValueError("Please enter valid email format")
        errors.append("Please enter valid email format")
        
    if not AuthHandler.check_valid_password(input.password):
        errors.append("Please enter a combination of special char, number, uppercase and lowercase characters with at least 12 characters")
        # raise ValueError("Please enter a combination of special char, number, uppercase and lowercase characters with at least 12 characters")
    return errors



@strawberry.type(description="Handles user-related authentication mutations")
class AuthMutation:
    
    @strawberry.mutation( description="Register a new user. Takes user input (first name, last name, email, password), "
                    "creates a new user in the database, and sends a verification email with a token link"
    )
    def register(self, input: RegisterInput) -> AuthSucess:
        session = db.get_session()

        
        # Validate input
        validate_errors = validate_register_input(input)

        if validate_errors:
            # return RegisterUserResponse(errors=[RegisterUserError(message=error) for error in validate_errors] , statusCode=409)
            raise AuthError(message="Email or password is not valid", code=status.HTTP_400_BAD_REQUEST, detail="Make sure your email is valid and your password is strong and at least 12 characters")
        
        # Check for existing user
        existing_user = DatabaseHandler.get_user_by_email(session, input.email)
        if existing_user:
            # return RegisterUserResponse(errors=[RegisterUserError(message="Existing email")], statusCode=409)
            raise AuthError(message="Existing email", code=status.HTTP_409_CONFLICT)

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
        register_token = JWTHandler.create_signup_token(new_user.id)
        EmailHandler.send_verification_email(token=register_token, user_email=new_user.email)

        
        return AuthSucess(token=register_token,code=status.HTTP_201_CREATED, message="Created user successfully")

       

        
        
    @strawberry.mutation
    def login(self, input:LoginInput, info:Info) -> AuthSucess:
        if info.context.get("user"):
            raise AuthError(message="This email already logged in", code=status.HTTP_400_BAD_REQUEST)
            # return LoginUserResponse(errors=[LoginUserError(message="Already Logged in")], statusCode=403)
        session = db.get_session()
        user = DatabaseHandler.get_user_by_email(session=session, email=input.email)
        
        if not user :
            raise AuthError(message="User does not exist", code=status.HTTP_404_NOT_FOUND)
        
        if user.password == None:
            raise AuthError(message="User already registered with another provider", code=status.HTTP_409_CONFLICT, detail="Please sign in using the provider")
        
        password_matched = AuthHandler.verify_password(hashed_password=user.password, password=input.password)
        if not password_matched:
            # return LoginUserResponse(errors=[LoginUserError(message="Invalid credential")], statusCode=401)
            raise AuthError(message="Email or password does not match", code=status.HTTP_401_UNAUTHORIZED)
        
        if not user.email_verified:
            # return LoginUserResponse(errors=[LoginUserError(message="Please verify your email account before continue")], statusCode=401)
            raise AuthError(message="Please verify your email account before continuing", code=403, detail="Check you email inbox to confirm your email address")
        login_token = JWTHandler.create_login_token(id=user.id)
        
        
        #Send login cookies to user (HTTP Only)
        response:Response = info.context["response"]
        response.set_cookie("auth_token", login_token, httponly=True)

        return AuthSucess(token=login_token, message="Logged in successfully", code=status.HTTP_200_OK)
    
    @strawberry.mutation
    async def googleLogin(self, input:GoogleLoginInput, info:Info) ->AuthSucess:
        
        if info.context.get("user"):
            raise AuthError(message="This email already logged in", code=status.HTTP_400_BAD_REQUEST)
        
        session = db.get_session()
        google_idInfo = await AuthHandler.verify_google_token(input.idToken)
        payload = {
            'firstName':google_idInfo.get("given_name"),
            'lastName':google_idInfo.get("family_name"),
            'id':google_idInfo.get("sub"),
            "email_verified":google_idInfo.get("email_verified"),
            'email':google_idInfo.get("email")
         }
        user = None
        
        existing_user = DatabaseHandler.get_user_by_email(session=session,email=payload.get("email"))
        
        if existing_user:
            user = existing_user
        else:
            new_user = UserModel(
                firstName=payload.get("firstName"), 
                lastName = payload.get('lastName'), 
                email=payload.get("email"), 
                email_verified = payload.get("email_verified")
                )
            DatabaseHandler.create_new_user(session=session, user_doc=new_user)
            
            auth_provider_doc = AuthProviderModel(id=payload.get("id"), user_id=new_user.id, name=AuthProviderName.GOOGLE)
            
            try:
                session.add(auth_provider_doc)
                new_user.auth_provider_id = payload.get("id")
                session.commit()
                session.refresh(auth_provider_doc)
            except Exception as e:
                print("Create Auth Provider Record FAIL")
                raise e
            user = new_user
        
        login_token = JWTHandler.create_login_token(user.id)
        response:Response = info.context["response"]
        response.set_cookie("auth_token", login_token, httponly=True)
        return AuthSucess(token=login_token, message="Logged in successfully", code=status.HTTP_200_OK)
    
    @strawberry.mutation
    @login_required
    def logout(self,info:Info)->None:
        user:UserModel = info.context.get('user')
        if user:
            info.context['user'] = None
            response: Response = info.context["response"]
            response.delete_cookie("auth_token")
    
    @strawberry.mutation
    def verify_email(self, input:VerifyEmailInput) -> None:
        # session = db.get_session()
        result = AuthHandler.verify_email(token=input.token)
        if result.get("status_code") != 200:
            raise AuthError(code=result.get("status_code"), message=result.get("message"))
        
        
        
        
            

        
        