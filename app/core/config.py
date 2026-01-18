import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vibe Matcher AI"
    API_V1_STR: str = "/api/v1"
    
    # OpenAI
    OPENAI_API_KEY: str = "sk-placeholder"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # ChromaDB
    CHROMA_DB_DIR: str = "chroma_db"
    COLLECTION_NAME: str = "fashion_products"
    
    # App
    DEBUG_MODE: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()
