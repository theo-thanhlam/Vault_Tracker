from fastapi import APIRouter,Depends
from .providers.google import google_router
from fastapi.responses import RedirectResponse
from ...graphql import auth_graphql_router
from ...utils.handler import AuthHandler
from ...utils import session




auth_router = APIRouter()
auth_router.include_router(google_router, prefix="/google")
auth_router.include_router(auth_graphql_router, prefix="/auth")




@auth_router.get("/verify-email",description="Verify email route")
def verify_email(token:str):
    AuthHandler.verify_email(token)
    return RedirectResponse("/")


    