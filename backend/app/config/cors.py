
origins = [
    "http://localhost:3000"
]
class CorsConfig:
    ORIGINS = origins
    ALLOW_METHODS=["*"]
    ALLOW_HEADERS=["*"]
    ALLOW_CREDENTIALS=True

cors_config = CorsConfig()