from fastapi import APIRouter,Depends, HTTPException,status
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
    result = AuthHandler.verify_email(token)
    if result.status_code == 400:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.message)
    if result.status_code == 401:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=result.message)
    if result.status_code == 201:
        return RedirectResponse("/")
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unavailable services")


    