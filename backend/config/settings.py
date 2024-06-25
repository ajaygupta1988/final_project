from pathlib import Path
from os import getenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from typing import Optional

BASE_DIR = Path(__file__).parent.resolve()
load_dotenv(dotenv_path=f"{BASE_DIR}/.env")


class Settings(BaseSettings):
    database_url: str = getenv("DATABASE_URL", "")
    database_tls: bool = getenv("DATABASE_TLS", True)
    database: str = getenv("DATABASE", "coredb")
    vantage_key: str = getenv("VANTAGE_KEY", "demo")
    queue_url: str = getenv("QUEUE_URL", None)
    collector_service_url: str = getenv("COLLECTOR_SERVICE_URL")
    aws_sqs_endpoint: str = getenv("AWS_SQS_ENDPOINT", "http://localhost:4566")


settings = Settings()
