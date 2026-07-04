import os
import argparse
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class Settings(BaseSettings):
    """Application settings with environment-based configuration."""

    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Application
    APP_NAME: str = "DocuGen API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8080

    # API
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./docugen.db"

    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS - stored as comma-separated string
    CORS_ORIGINS_STR: str = "http://localhost:5173,http://localhost:3000"

    @computed_field
    @property
    def CORS_ORIGINS(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS_STR.split(",")]


def get_settings(env: str = "local") -> Settings:
    """Load settings from environment-specific file."""
    env_path = f"env/.env.{env}"

    if not os.path.exists(env_path):
        print(f"Warning: Environment config file {env_path} does not exist")
        print(f"Using default settings for environment: {env}")
        return Settings()

    return Settings(_env_file=env_path)


def parse_args():
    """Parse command-line arguments for environment selection."""
    parser = argparse.ArgumentParser(description="FastAPI Application")
    parser.add_argument(
        "--env",
        type=str,
        default="local",
        choices=["local", "dev", "staging", "prod"],
        help="Environment to run the application (default: local)",
    )
    args, unknown = parser.parse_known_args()
    return args


# Initialize settings
args = parse_args()
settings = get_settings(args.env)
