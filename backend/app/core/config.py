from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "SmartSpend"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"

    database_url: str = "postgresql+asyncpg://smartspend:smartspend@db:5432/smartspend"
    database_url_sync: str = "postgresql+psycopg2://smartspend:smartspend@db:5432/smartspend"

    redis_url: str = "redis://redis:6379/0"
    celery_broker_url: str = "redis://redis:6379/1"
    celery_result_backend: str = "redis://redis:6379/2"

    upload_dir: str = "/tmp/smartspend_uploads"
    max_upload_size_mb: int = 20


settings = Settings()
