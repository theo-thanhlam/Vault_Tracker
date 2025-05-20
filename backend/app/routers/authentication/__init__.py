from fastapi import APIRouter,Depends, HTTPException,status
from .providers.google import google_router
from fastapi.responses import RedirectResponse
from ...api import auth_graphql_router
from ...utils.handler import AuthHandler
from ...utils import session




# auth_router = APIRouter(prefix="/auth")
# auth_router.include_router(google_router, prefix="/google")
# auth_router.include_router(auth_graphql_router, prefix="/gql")







    