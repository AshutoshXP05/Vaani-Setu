from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = 'Vaani Setu'
    ENVIRONMENT: str = 'development'
    DATABASE_URL: str = 'sqlite:///./vaani_setu.db'

    LLM_PROVIDER: str = 'groq'
    LLM_API_KEY: str = ''
    LLM_MODEL_NAME: str = ''

    AGENT_MAX_TOOL_CALLS: int = 5

    EMBEDDING_MODEL_NAME: str = 'intfloat/multilingual-e5-base'

    JWT_SECRET_KEY: str = 'jwt-secret-key'
    JWT_ALGORITHM: str = 'HS256'
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()