from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Required settings
    openai_api_key: str
    redis_host: str = "redis"
    redis_port: int = 6379

    # Optional settings that might be injected by Coolify
    source_commit: Optional[str] = None
    pythonpath: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None

    class Config:
        env_file = ".env"
        extra = "ignore"  # This will ignore any extra environment variables

settings = Settings()