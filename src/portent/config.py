import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv(override=False)


@dataclass(frozen=True)
class Settings:
    token: str = os.getenv("TOKEN", "")
    dev_guild_id: int | None = int(os.getenv("DEV_GUILD_ID")) if os.getenv("DEV_GUILD_ID") else None
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    sync_mode: str = os.getenv("SYNC_MODE", "guild")
    app_id: int | None = int(os.getenv("APP_ID")) if os.getenv("APP_ID") else None


settings = Settings()
