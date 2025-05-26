import redis
from ..config.redis import redis_config
from .handler import JWTHandler, DatabaseHandler
from . import db
from ..models import UserModel
from datetime import datetime



def get_redis():
    connection_pool = redis_config.get_connection_pool() 
    return redis.Redis(connection_pool=connection_pool)

def get_current_user(token:str=None)->UserModel | None:
   
    session = db.get_session()
    decoded_token = JWTHandler.verify_login_token(token)
    
    if decoded_token:
        now = datetime.now()
        token_expire_date = datetime.fromtimestamp(decoded_token.get('exp'))
        if(now < token_expire_date):
            user = DatabaseHandler.get_user_by_id(session=session, id=decoded_token.get("id"))
            return user
    return None

