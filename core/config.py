# from os import getenv
from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import BaseModel
BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / "db.sqlite3"


class DBSettings(BaseModel):
    db_url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    db_echo: bool = False


class Setting(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    db_echo: bool = False


settings = Setting()
