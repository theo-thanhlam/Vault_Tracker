from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from ....utils.oauth import oauth, callback_handler
from strawberry import Info


google_router = APIRouter()


@google_router.get("/login")
async def login(request:Request):
    redirect_uri = request.url_for('callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)
    

@google_router.get("/callback")
async def callback(request:Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        
        # resp = await oauth.google.get('userinfo', token=token)
        # user_info = resp.json()      
        
        # login_token = callback_handler(callback_token=token, user_info=user_info)
        
        response:Response = RedirectResponse("/")
        
        # response.set_cookie("access_token", login_token, httponly=True)
        print(token)
        
        
    except Exception as err:
        print(err)
        response = RedirectResponse("/auth/google/login")
    return response
    
     