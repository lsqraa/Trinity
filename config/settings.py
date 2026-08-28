from __future__ import annotations
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass


class Settings:
    BASE_DIR: Path = BASE_DIR

    @property
    def PLAYWRIGHT_USER_DATA_DIR(self) -> str:
        return os.getenv("PLAYWRIGHT_USER_DATA_DIR", str(BASE_DIR / "data" / "browser_session"))

    @property
    def PLAYWRIGHT_HEADLESS(self) -> bool:
        return os.getenv("PLAYWRIGHT_HEADLESS", "False").lower() in ("true", "1", "yes")

    @property
    def WHATSAPP_URL(self) -> str:
        return os.getenv("WHATSAPP_URL", "https://web.whatsapp.com/")

    @property
    def LOGIN_TIMEOUT_SEC(self) -> int:
        return int(os.getenv("LOGIN_TIMEOUT_SEC", "900"))

    @property
    def MIN_DELAY_SECONDS(self) -> float:
        return float(os.getenv("MIN_DELAY_SECONDS", "2.0"))

    @property
    def MAX_DELAY_SECONDS(self) -> float:
        return float(os.getenv("MAX_DELAY_SECONDS", "5.0"))

    @property
    def DAILY_MESSAGE_LIMIT(self) -> int:
        return int(os.getenv("DAILY_MESSAGE_LIMIT", os.getenv("MAX_DAILY_QUOTA", "45")))

    @property
    def MAX_DAILY_QUOTA(self) -> int:
        return self.DAILY_MESSAGE_LIMIT


settings = Settings()
