from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.cors import cors_config
from .utils import session
from .graphql import graphql_router
from .utils.db import get_engine,get_session
from .models.base import Base
from fastapi import Request, HTTPException
from .utils.auth import JWTHandler
from .models import UserModel,VerificationModel
from fastapi.responses import RedirectResponse

app = FastAPI()

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.ORIGINS,
    allow_credentials=cors_config.ALLOW_CREDENTIALS,
    allow_methods=cors_config.ALLOW_METHODS,
    allow_headers=cors_config.ALLOW_HEADERS
)

#Routers

@app.on_event("startup")
def startup():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    
    pass


@app.get("/verify-email")
def verify_email(token:str):

    try:
        # Check if register token exists in database
        session = get_session()
        token_existed = session.get(VerificationModel, token)
        if not token_existed:
            return {"message":"Invalid Token"}
        
        #Check valid token
        decoded_token=JWTHandler.verify_signup_token(token=token)
        if not decoded_token:
            return {"message":"Invalid token"}
        
        user_id = decoded_token.get("id")
        user = session.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_verified:
            return {"message": "User already verified"}

        user.is_verified = True
        session.commit()

        return {"message": "Email verified successfully"}
        
        
        
        
    except Exception as e:
        pass


@app.get("/")
def root():
    return {"message": "Hello World"}



app.include_router(graphql_router, prefix='/graphql')

