# TechStore Telegram AI Assistant

A Telegram bot that acts as an AI sales consultant for a monitor shop. It helps users choose a product from a fixed catalog, guides them through checkout, and saves confirmed orders to Google Sheets.

Built with **Python 3.12**, **pyTelegramBotAPI** (`telebot`), **OpenAI API**, **gspread**, and **python-dotenv**.

---

## Features

### AI assistant
- Conversational consultant powered by OpenAI Chat Completions
- Per-user chat history for multi-turn dialogue
- Built-in product catalog and system prompt that define consultation and checkout behavior
- Recommendations limited to in-catalog items only

### Order system
- Structured flow: needs → product choice → customer details → confirmation
- Order is finalized when the model marks the dialog with `[COMPLETE]`
- Order fields are extracted from the conversation via a separate AI call (`extract_order`)
- Saved fields: name, contact, model, quantity, address, payment, Telegram user ID, source
  
### Google Sheets integration
- Confirmed orders are appended to a spreadsheet via a Google service account
- Optional: if `GOOGLE_SHEET_ID` is not set, the bot still runs but skips sheet writes

---

## Related Projects

This Telegram assistant is part of a multi-channel AI sales system.

The project shares the same Google Sheets database with the web version of the assistant.

```text
Telegram AI Assistant ──┐
                        │
                        ▼
                  Google Sheets
                        ▲
                        │
Flask Web Assistant ────┘
```

The `source` column is used to identify where an order originated.

| Source   | Description           |
| -------- | --------------------- |
| telegram | Telegram AI Assistant |
| website  | Flask Web Application |

Related repository:

* [AI Monitor Sales Assistant (Web)](https://github.com/VikkMoor/ai_chat_website)

---

## Project structure

```
telegram_ai_assistant/
├── bot.py           # Telegram handlers, session history, order trigger
├── ai_logic.py      # OpenAI prompts, replies, order extraction
├── sheets.py        # Google Sheets client (order logging)
├── config.py        # Environment variables and validation
├── requirements.txt
├── .gitignore
└── README.md
```

| Module | Responsibility |
|--------|----------------|
| `bot.py` | `/start`, text messages, history management, order save on `[COMPLETE]` |
| `ai_logic.py` | Catalog, system prompt, `get_ai_reply()`, `extract_order()` |
| `sheets.py` | `append_order()` — writes one row per confirmed order |
| `config.py` | Loads `.env`, exposes settings, validates required keys |

---

## Requirements

- Python 3.12
- [Telegram Bot Token](https://t.me/BotFather)
- [OpenAI API key](https://platform.openai.com/)
- (Optional) Google Cloud service account with Sheets API access

---

## Setup

### 1. Clone and install dependencies

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

GOOGLE_CREDENTIALS_PATH=credentials.json
GOOGLE_SHEET_ID=your_spreadsheet_id
GOOGLE_SHEET_WORKSHEET=Sheet1
```

`TELEGRAM_BOT_TOKEN` and `OPENAI_API_KEY` are required. Google Sheets variables are optional.

### 3. Google Sheets (optional)

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/).
2. Enable **Google Sheets API** and **Google Drive API**.
3. Create a service account and download the JSON key as `credentials.json`.
4. Share the target spreadsheet with the service account email (Editor access).
5. Add a header row on the worksheet:

   `created_at | name | contact | model | quantity | address | payment | telegram_id | source`

6. Set `GOOGLE_SHEET_ID` (from the spreadsheet URL) and `GOOGLE_SHEET_WORKSHEET` in `.env`.

Do not commit `.env` or `credentials.json` to version control.

### 4. Run the bot

```bash
python bot.py
```

Send `/start` in Telegram to begin a new consultation session.

---

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes | Bot token from BotFather |
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `OPENAI_MODEL` | No | Model name (default: `gpt-4o-mini`) |
| `GOOGLE_CREDENTIALS_PATH` | No* | Path to service account JSON (default: `credentials.json`) |
| `GOOGLE_SHEET_ID` | No* | Spreadsheet ID for order logging |
| `GOOGLE_SHEET_WORKSHEET` | No* | Worksheet name (default: `Sheet1`) |

\*Required only if you want orders saved to Google Sheets.

---

## How it works

1. User sends `/start` — conversation history is reset and the bot asks about use case (gaming, work, design, etc.).
2. User messages are appended to session history and sent to OpenAI with the TechStore system prompt.
3. The assistant collects requirements, suggests monitors from the catalog, and gathers delivery/payment details.
4. After user confirmation, the model responds with `[COMPLETE]` on the last line.
5. `extract_order()` parses the dialog into structured JSON; `append_order()` writes a row to Google Sheets.

---

## Dependencies

See `requirements.txt`:

- `pyTelegramBotAPI` — Telegram Bot API
- `openai` — OpenAI client
- `gspread`, `google-auth` — Google Sheets
- `python-dotenv` — `.env` loading

---

## Author note

This project was developed as an academic demonstration of integrating conversational AI, a Telegram interface, and external data storage (Google Sheets) in a single Python application.
