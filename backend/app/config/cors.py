

class CorsConfig:
    ORIGINS = ["*"]
    ALLOW_METHODS=["*"]
    ALLOW_HEADERS=["*"]
    ALLOW_CREDENTIALS=True

cors_config = CorsConfig()