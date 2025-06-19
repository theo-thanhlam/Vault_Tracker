import os
from dotenv import load_dotenv

load_dotenv()

def get_environment() -> str:
    env = os.getenv("ENVIRONMENT")
    return env