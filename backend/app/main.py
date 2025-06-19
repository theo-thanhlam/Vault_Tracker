from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .config.cors import cors_config
from .utils import session
from .api import graphql_router
from .utils.db import get_engine,get_session
from .models.base import Base
from fastapi import Request, HTTPException
from .utils.handler import JWTHandler
from .models.core import UserModel,TokenModel
from starlette.middleware.sessions import SessionMiddleware
# from .routers.authentication import auth_router

app = FastAPI()

#Middlewares

## CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.ORIGINS,
    allow_credentials=cors_config.ALLOW_CREDENTIALS,
    allow_methods=cors_config.ALLOW_METHODS,
    allow_headers=cors_config.ALLOW_HEADERS,
    # credentials=True
)

## Session
app.add_middleware(SessionMiddleware, secret_key = "whlM5uIw+qslOOz1jISxECKTsR1t09bDoOVKUMQkKj2NhSoMG2fTCIf1NSqkzVzJ")


#Routers

@app.on_event("startup")
def startup():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    
    pass




@app.get("/")
def root():
    return {"message": "Hello World"}



app.include_router(graphql_router, prefix='/gql')