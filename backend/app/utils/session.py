import redis
from ..config.redis import redis_config



def get_redis():
    connection_pool = redis_config.get_connection_pool() 
    return redis.Redis(connection_pool=connection_pool)

    