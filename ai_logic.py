"""
Логика общения с OpenAI API.
"""

from openai import OpenAI

import config

# Клиент создаётся один раз при импорте модуля
_client = OpenAI(api_key=config.OPENAI_API_KEY)

# Системный промпт — задаёт поведение ассистента
DEFAULT_SYSTEM_PROMPT = (
    "Ты полезный ассистент в Telegram-боте. "
    "Отвечай кратко и по делу на языке пользователя."
)


def get_ai_reply(user_message: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> str:
    """
    Отправляет сообщение пользователя в Chat Completions и возвращает ответ модели.

    :param user_message: текст от пользователя
    :param system_prompt: инструкция для модели
    :return: текст ответа ассистента
    """
    response = _client.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content or ""
