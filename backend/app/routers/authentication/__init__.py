from fastapi import APIRouter
from .providers.google import google_router
from fastapi.responses import RedirectResponse
from ...graphql import auth_graphql_router

auth_router = APIRouter(prefix="/auth")
auth_router.include_router(google_router, prefix="/google")
auth_router.include_router(auth_graphql_router, prefix="/manual")

@auth_router.get("/")
def index():
    return RedirectResponse("/")
