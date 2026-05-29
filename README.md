# Telegram AI Assistant

Telegram-бот на Python 3.12 с ответами через OpenAI и опциональным логированием диалогов в Google Sheets.

## Структура проекта

```
telegram_ai_assistant/
├── bot.py              # Telegram-бот (handlers, polling)
├── ai_logic.py         # Запросы к OpenAI API
├── sheets.py           # Запись диалогов в Google Sheets
├── config.py           # Загрузка настроек из .env
├── requirements.txt
├── .env.example
└── README.md
```

## Требования

- Python 3.12
- Токен бота ([@BotFather](https://t.me/BotFather))
- API-ключ [OpenAI](https://platform.openai.com/)
- (Опционально) Google Cloud service account и таблица для gspread

## Установка

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Заполните `.env` своими значениями.

### Google Sheets (опционально)

1. Создайте проект в [Google Cloud Console](https://console.cloud.google.com/).
2. Включите Google Sheets API и Google Drive API.
3. Создайте сервисный аккаунт и скачайте JSON-ключ → сохраните как `credentials.json`.
4. Откройте таблицу и выдайте сервисному аккаунту доступ «Редактор».
5. В первой строке листа задайте заголовки:  
   `timestamp | user_id | username | user_message | bot_reply`
6. Укажите `GOOGLE_SHEET_ID` и `GOOGLE_SHEET_WORKSHEET` в `.env`.

Если `GOOGLE_SHEET_ID` пустой, бот работает без записи в таблицу.

## Запуск

```bash
python bot.py
```

## Переменные окружения

| Переменная | Описание |
|------------|----------|
| `TELEGRAM_BOT_TOKEN` | Токен Telegram-бота |
| `OPENAI_API_KEY` | Ключ OpenAI API |
| `OPENAI_MODEL` | Модель (по умолчанию `gpt-4o-mini`) |
| `GOOGLE_CREDENTIALS_PATH` | Путь к JSON сервисного аккаунта |
| `GOOGLE_SHEET_ID` | ID Google-таблицы |
| `GOOGLE_SHEET_WORKSHEET` | Имя листа |

## Лицензия

MIT (при необходимости укажите свою).
