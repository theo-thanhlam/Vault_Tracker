from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth
import authlib
from strawberry import Info
import os
from . import db
from ..models import *
from .handler import *
from ..models import UserModel, AuthProviderModel, AuthProviderName
load_dotenv()

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri= "https://www.googleapis.com/oauth2/v3/certs",
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

def callback_handler(callback_token:authlib.oauth2.rfc6749.wrappers.OAuth2Token,user_info:dict[str,any])->str|None:
    session = db.get_session()
    # session.rollback()
    
    payload = {
        'firstName':user_info.get("given_name"),
        'lastName':user_info.get("family_name"),
        'id':user_info.get("id"),
        "email_verified":user_info.get("verified_email"),
        'email':user_info.get("email")
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
    
    return login_token