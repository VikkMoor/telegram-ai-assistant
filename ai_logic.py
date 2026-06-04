"""
Логика общения с OpenAI API.
"""

import json

from openai import OpenAI

import config


# Клиент создаётся один раз при импорте модуля
_client = OpenAI(api_key=config.OPENAI_API_KEY)

PRODUCT_CATALOG = """
Samsung Odyssey G7 32" — 45 990 ₽
• 2560x1440 (QHD), VA, 240 Гц, 1 мс
• Изогнутый экран 1000R, HDR600
• Для киберспорта и динамичных игр

LG UltraGear 27GP850 — 38 500 ₽
• 27", QHD, Nano IPS, 165 Гц, 1 мс
• G-Sync Compatible, HDR400
• Игры + графика

Dell UltraSharp U2723DE — 52 900 ₽
• 27", QHD, IPS Black, 60 Гц
• USB-C 90W, точная цветопередача
• Работа / дизайн / офис

ASUS TUF Gaming VG27AQ — 29 990 ₽
• 27", QHD, IPS, 165 Гц, 1 мс
• HDR10, G-Sync Compatible
• Универсальный гейминг

BenQ SW270C — 48 500 ₽
• 27", QHD, IPS, Adobe RGB 99%
• Аппаратная калибровка
• Фото / видео / цветокор

AOC 24G2U — 16 990 ₽
• 24", Full HD, IPS, 144 Гц
• Бюджетный гейминг

Xiaomi Mi Curved 34" — 32 900 ₽
• 34", UltraWide 3440x1440, 144 Гц
• Многозадачность + игры

ViewSonic VP2468a — 24 500 ₽
• 24", Full HD, IPS, ΔE<2
• Работа с документами

MSI Optix MAG274QRF-QD — 42 990 ₽
• 27", QHD, Quantum Dot IPS, 165 Гц
• Цвет + гейминг

HP E27 G4 — 21 900 ₽
• 27", Full HD, IPS, 75 Гц
• Офис / учёба
"""

# Системный промпт — задаёт поведение ассистента
DEFAULT_SYSTEM_PROMPT = f"""
Ты профессиональный консультант интернет-магазина мониторов TechStore.

Вот каталог доступных товаров:

{PRODUCT_CATALOG}

Твоя задача — помогать пользователю выбрать подходящий монитор и оформить заказ.

ЭТАП 1. Выявление потребностей

* Узнай, для каких задач нужен монитор (игры, работа, дизайн, универсальное использование).
* Уточни бюджет.
* Уточни предпочтительный размер экрана и важные характеристики.

ЭТАП 2. Консультация

* Предлагай только модели из каталога.
* Рекомендуй 2–3 подходящих варианта.
* Кратко объясняй различия между ними.
* Помогай пользователю выбрать наиболее подходящую модель.

ЭТАП 3. Оформление заказа
После выбора товара собери:

* имя клиента;
* контактный телефон;
* выбранную модель;
* количество;
* адрес доставки;
* способ оплаты.

Не придумывай данные за клиента.
Если какой-либо информации не хватает, обязательно задай уточняющий вопрос.

ЭТАП 4. Подтверждение заказа

* Повтори все данные заказа.
* Попроси клиента подтвердить заказ.
* Подтверждением считаются сообщения вроде:
  "подтверждаю",
  "да",
  "всё верно",
  "верно".

ПРАВИЛА ОБЩЕНИЯ

* Общайся дружелюбно и профессионально.
* Отвечай кратко и по существу.
* Используй только информацию из каталога.
* Не выдумывай товары и характеристики.
* Если пользователь спрашивает о товаре, которого нет в каталоге, вежливо сообщи об этом.
* Всегда отвечай на языке пользователя.

ФИКСАЦИЯ ГОТОВОГО ЗАКАЗА

Когда собраны ВСЕ данные:

* имя клиента;
* контакт;
* модель;
* количество;
* адрес доставки;
* способ оплаты;

и клиент подтвердил заказ,

ты ОБЯЗАН:

1. Подтвердить оформление заказа.
2. На отдельной последней строке вывести строго:

[COMPLETE]

После метки [COMPLETE] ничего больше не добавляй.
"""



def get_ai_reply(messages: list, system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> str:
    response = _client.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            *messages,
        ],
    )

    return response.choices[0].message.content or ""


def _normalize_order(data: dict) -> dict:
    """Приводит результат к безопасной структуре."""
    fields = ["name", "contact", "model", "quantity", "address", "payment"]

    return {
        field: (data.get(field) or "").strip() if isinstance(data.get(field), str) else ""
        for field in fields
    }

def extract_order(dialog_history: list) -> dict:
    response = _client.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": """
Извлеки данные заказа из диалога.

Верни ТОЛЬКО валидный JSON.

Правила:
- Если значение отсутствует — используй ""
- НИКОГДА не пиши "не указан", "нет", "unknown"
- НЕ придумывай данные
- НЕ интерпретируй пользователя

Формат:

{
    "name": "",
    "contact": "",
    "model": "",
    "quantity": "",
    "address": "",
    "payment": ""
}
"""
            },
            *dialog_history,
        ],
    )

    content = response.choices[0].message.content or "{}"

    print("\n========== RAW JSON ==========")

    print(content)
    print("========== END RAW JSON ==========\n")

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        print("JSON DECODE ERROR")
        return _normalize_order({})

    return _normalize_order(data)

