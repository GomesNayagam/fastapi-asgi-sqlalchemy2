from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    root_path: str = ""
    echo_sql: bool = True
    logging_level: str = "INFO"
    shared_memory_dir: str = "/tmp/shm"
    database_url: str
    auth_check: bool = True
    expected_audience: str = ""
    expected_issuer: str = ""
    jwks_uri: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
