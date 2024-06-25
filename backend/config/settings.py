from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.resolve()


class Settings(BaseSettings):
    database_url: str
    database_tls: bool
    database: str
    vantage_key: str

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


settings = Settings()
