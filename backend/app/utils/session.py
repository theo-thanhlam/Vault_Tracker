import redis
from ..config.redis import redis_config
from .auth import JWTHandler, DatabaseHandler
from . import db
from fastapi import HTTPException,status


def get_redis():
    connection_pool = redis_config.get_connection_pool() 
    return redis.Redis(connection_pool=connection_pool)

def get_current_user(token:str=None):
    session = db.get_session()
    
    decoded_token = JWTHandler.verify_login_token(token)
    if not decoded_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    
    user = DatabaseHandler.get_user_by_id(session=session, id=decoded_token.get("id"))
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not verified")
    
    return user
    