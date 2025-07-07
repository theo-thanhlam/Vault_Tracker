from dotenv import load_dotenv
import os
load_dotenv()

origins = [
   os.getenv("FRONTEND_URL")
]
class CorsConfig:
    ORIGINS = origins
    ALLOW_METHODS=["*"]
    ALLOW_HEADERS=["*"]
    ALLOW_CREDENTIALS=True

cors_config = CorsConfig()