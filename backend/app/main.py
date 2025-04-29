from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import cors
from .utils.db import get_engine, SQLModel
from .graphql import graphql_app


app = FastAPI()

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors.ORIGINS,
    allow_credentials=cors.ALLOW_CREDENTIALS,
    allow_methods=cors.ALLOW_METHODS,
    allow_headers=cors.ALLOW_HEADERS
)

#Routers

@app.on_event("startup")
def startup():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
    # pass
    
    


@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(graphql_app, prefix='/graphql')