from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    llm_api_key: str | None = None
    llm_model: str = "gpt-4o-mini"
    database_url: str = "sqlite:///./resume_analyzer.db"
    max_upload_mb: int = 5
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
