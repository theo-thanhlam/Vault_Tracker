from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import cors
from .routers import users



a = 1
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
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}