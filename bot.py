"""
Точка входа: Telegram-бот на pyTelegramBotAPI (telebot).
"""

import logging

import telebot
from telebot import types

import ai_logic
import config
import sheets

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

config.validate_config()
bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start", "help"])
def handle_start(message: types.Message) -> None:
    """Приветствие и краткая справка."""
    bot.reply_to(
        message,
        "Привет! Я AI-ассистент.\n"
        "Напиши любой вопрос — отвечу с помощью OpenAI.\n"
        "Команды: /start, /help",
    )


@bot.message_handler(content_types=["text"])
def handle_text(message: types.Message) -> None:
    """Обрабатывает текстовые сообщения: AI-ответ и опционально запись в Sheets."""
    user_text = (message.text or "").strip()
    if not user_text:
        return

    # Показываем, что бот «печатает»
    bot.send_chat_action(message.chat.id, "typing")

    try:
        reply = ai_logic.get_ai_reply(user_text)
    except Exception:
        logger.exception("Ошибка OpenAI API")
        bot.reply_to(message, "Не удалось получить ответ. Попробуйте позже.")
        return

    bot.reply_to(message, reply)

    # Сохраняем диалог в Google Sheets (если настроено)
    try:
        sheets.append_dialog_row(
            user_id=message.from_user.id,
            username=message.from_user.username,
            user_message=user_text,
            bot_reply=reply,
        )
    except Exception:
        logger.exception("Ошибка записи в Google Sheets")


def main() -> None:
    """Запуск long polling."""
    logger.info("Бот запущен")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
