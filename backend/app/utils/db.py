from sqlmodel import create_engine,SQLModel, Session
from dotenv import load_dotenv
from ..models import UserModel

import os

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL")

_engine = create_engine(DATABASE_URL, echo=True)
def get_engine():
    return _engine


