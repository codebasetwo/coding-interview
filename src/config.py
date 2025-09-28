from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    API_PREFIX: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    PASSWORD_RESET_VERIFICATION_LINK: str
    REDIS_URL: str
    JWT_SECRETE: str
    JWT_ALGORITHM: str
    VERIFICATION_LINK: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_FROM: str
    MAIL_FROM_NAME: str

    model_config = SettingsConfigDict(env_file=".env")


Config = Settings()

# Broker URL
broker_url = Config.REDIS_URL
# Backend for storing task results
result_backend = Config.REDIS_URL
broker_connection_retry_on_startup = True