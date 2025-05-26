from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


import os

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL")
POOL_SIZE=10
MAX_OVERFLOW = 20
POOL_RECYCLE= 1800 # 1800 seconds = 30 minute
POOL_PRE_PING = True
_engine = create_engine(DATABASE_URL, pool_pre_ping=POOL_PRE_PING, pool_size = POOL_SIZE, max_overflow=MAX_OVERFLOW, pool_recycle=POOL_RECYCLE)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=_engine)

def get_engine():
    return _engine

def get_session():
    return SessionLocal()
    


