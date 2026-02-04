from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/mvp"

    class Config:
        env_prefix = ""


settings = Settings()
engine = create_engine(settings.database_url, poolclass=NullPool)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
