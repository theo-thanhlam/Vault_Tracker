
origins = [
    "http://localhost:3000",
    "http://137.184.161.82:3000"
]
class CorsConfig:
    ORIGINS = origins
    ALLOW_METHODS=["GET, POST, OPTIONS"]
    ALLOW_HEADERS=["*"]
    ALLOW_CREDENTIALS=True

cors_config = CorsConfig()