from enum import Enum
import os
from dotenv import load_dotenv

load_dotenv()


class MissingEnvironmentVariable(Exception):
    pass


class DatabaseType(Enum):
    SQLITE = "sqlite"
    POSTGRES = "postgres"


def get_required_env_var(key: str) -> str:
    value = os.getenv(key)

    if not value:
        raise MissingEnvironmentVariable(f"Missing required environment variable {key}")

    return value


SOLAX_TOKEN_ID = get_required_env_var("SOLAX_TOKEN_ID")
SOLAX_SERIAL_NUMBER = get_required_env_var("SOLAX_SERIAL_NUMBER")
SOLAX_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"  # e.g. '2023-05-06 16:21:24'
P1_IP_ADDRESS = get_required_env_var("P1_IP_ADDRESS")

DATABASE_TYPE = DatabaseType(os.getenv("DATABASE", "sqlite"))

if DATABASE_TYPE == DatabaseType.POSTGRES:
    POSTGRES_USER = get_required_env_var("POSTGRES_USER")
    POSTGRES_PASSWORD = get_required_env_var("POSTGRES_PASSWORD")
    POSTGRES_HOST = get_required_env_var("POSTGRES_HOST")
    POSTGRES_PORT = int(get_required_env_var("POSTGRES_PORT"))
    POSTGRES_DATABASE_NAME = get_required_env_var("POSTGRES_DATABASE_NAME")
