"""
Работа с Google Sheets через gspread.
"""

from datetime import datetime, timezone
from typing import Any

import gspread
from google.oauth2.service_account import Credentials

import config

# Области доступа для сервисного аккаунта Google
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def _get_worksheet():
    """Открывает таблицу и возвращает лист по имени из конфига."""
    creds = Credentials.from_service_account_file(
        config.GOOGLE_CREDENTIALS_PATH,
        scopes=SCOPES,
    )
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(config.GOOGLE_SHEET_ID)
    return spreadsheet.worksheet(config.GOOGLE_SHEET_WORKSHEET)


def append_dialog_row(
    user_id: int,
    username: str | None,
    user_message: str,
    bot_reply: str,
) -> None:
    """
    Добавляет строку с диалогом в конец листа.

    Ожидаемые колонки (первая строка — заголовки):
    timestamp | user_id | username | user_message | bot_reply
    """
    if not config.GOOGLE_SHEET_ID:
        return  # логирование в Sheets отключено, если ID не задан

    worksheet = _get_worksheet()
    row: list[Any] = [
        datetime.now(timezone.utc).isoformat(),
        user_id,
        username or "",
        user_message,
        bot_reply,
    ]
    worksheet.append_row(row, value_input_option="USER_ENTERED")
