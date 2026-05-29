"""
Загрузка настроек из переменных окружения (.env).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Подгружаем .env из корня проекта
load_dotenv(Path(__file__).resolve().parent / ".env")

# Telegram
TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

# OpenAI
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Google Sheets (путь к JSON-ключу сервисного аккаунта)
GOOGLE_CREDENTIALS_PATH: str = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
GOOGLE_SHEET_ID: str = os.getenv("GOOGLE_SHEET_ID", "")
GOOGLE_SHEET_WORKSHEET: str = os.getenv("GOOGLE_SHEET_WORKSHEET", "Sheet1")


def validate_config() -> None:
    """Проверяет наличие обязательных переменных перед запуском бота."""
    missing: list[str] = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    if missing:
        raise ValueError(
            f"Не заданы переменные окружения: {', '.join(missing)}. "
            "Скопируйте .env.example в .env и заполните значения."
        )
