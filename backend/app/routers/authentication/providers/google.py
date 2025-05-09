from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from ....utils.oauth import oauth, callback_handler


google_router = APIRouter()


@google_router.get("/login")
async def login(request:Request):
    redirect_uri = request.url_for('callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)
    

@google_router.get("/callback")
async def callback(request:Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        resp = await oauth.google.get('userinfo', token=token)
        user_info = resp.json()      
        
        callback_handler(callback_token=token, user_info=user_info)
        return RedirectResponse("/")
    except Exception as err:
        print(err)
        return {"message":"Internal Server Errors"}