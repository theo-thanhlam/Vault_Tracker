from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth
import authlib
from strawberry import Info
import os
from . import db
from ..models import *
from jose import jwt

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

def callback_handler(callback_token:authlib.oauth2.rfc6749.wrappers.OAuth2Token,user_info:dict[str,any]):
    
    info_payload = {
        'firstName':user_info.get("given_name"),
        'lastName':user_info.get("family_name"),
        'id':user_info.get("id"),
        "email_verified":user_info.get("verified_email"),
        'email':user_info.get("email")
    }
    
    
    
    
    
    pass