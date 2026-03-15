import re
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from pydantic_settings import BaseSettings

from aiogram import Bot

load_dotenv()

class Settings(BaseSettings):
    BOT_TOKEN: str
    IS_PRODUCTION: bool
    LOGS_DIR: Path = Path(__file__).parent / "logs"
    ADMINS: List[int] = [6177013412, 1519003900]
    
    @property
    def DB_URI(self):
        BASE_PATH = "sqlite+aiosqlite:///database.db"
        if self.IS_PRODUCTION:
            return BASE_PATH
        return BASE_PATH
    
    @property
    def SYNC_DB_URI(self):
        return re.sub(r"\+?a\w+\+?", "", self.DB_URI, 1)

settings = Settings()

bot = Bot(settings.BOT_TOKEN)
engine = create_async_engine(settings.DB_URI)
session_factory = async_sessionmaker(
    bind = engine,
    expire_on_commit=False,
    autoflush=False
)