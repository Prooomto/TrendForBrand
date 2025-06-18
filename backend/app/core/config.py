from typing import Optional
from pydantic import BaseModel, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Base
    PROJECT_NAME: str = "TrendForBrand"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode='before')
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info) -> Optional[str]:
        if isinstance(v, str):
            return v
        
        # Получаем значения из info.data
        values = info.data
        user = values.get("POSTGRES_USER")
        password = values.get("POSTGRES_PASSWORD")
        server = values.get("POSTGRES_SERVER")
        db = values.get("POSTGRES_DB")
        port = values.get("POSTGRES_PORT", 5432)
        
        return f"postgresql+asyncpg://{user}:{password}@{server}:{port}/{db}"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env"
    )


settings = Settings() 