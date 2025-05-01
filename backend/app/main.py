from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.cors import cors_config
from .utils import session
from .graphql import graphql_router
from .utils.db import get_engine
from .models.base import Base


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


    
    


@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(graphql_router, prefix='/graphql')

