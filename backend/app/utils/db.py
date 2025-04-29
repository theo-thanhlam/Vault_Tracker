from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


import os

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL")

_engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=_engine)

def get_engine():
    return _engine

def get_session():
    return SessionLocal()
    


