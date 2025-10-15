import os
import re

from telegram.ext import Application, CommandHandler, MessageHandler, filters

# === Списки триггеров ===

BAD_WORDS = {
    'бля', 'блять', 'блядь', 'сука', 'сучка', 'пизда', 'пиздец', 'хуй', 'хуёвый', 'хуевый',
    'ебать', 'ёбать', 'нахуй', 'нахер', 'нахрен', 'заебал', 'заебись', 'охуел', 'охуенно',
    'гандон', 'говно', 'говнюк', 'мудак', 'мудила', 'лох', 'лошара', 'пидор', 'педик',
    'чмо', 'урод', 'скотина', 'сволочь', 'дрочить', 'дрочила', 'залупа', 'мразь'
}

UNDERSTAND_WORDS = {'понял', 'поняла'}
EAT_WORDS = {'есть'}

# === Вспомогательные функции ===

def clean_word(word):
    return re.sub(r'[^а-яё]', '', word.lower())

def text_to_words(text):
    return {clean_word(w) for w in text.split()}

def contains_bad_word(text):
    if not text:
        return False
    return bool(text_to_words(text) & BAD_WORDS)

def contains_understand_word(text):
    if not text:
        return False
    return bool(text_to_words(text) & UNDERSTAND_WORDS)

def contains_eat_word(text):
    if not text:
        return False
    # Ищем слово "есть" как отдельное слово (а не внутри "приветствую")
    words = re.findall(r'\b\w+\b', text.lower())
    return 'есть' in words

# === Обработчики ответов ===

async def reply_praise(update, context):
    await update.message.reply_text("Ты молодец! Держи конфетку!")

async def reply_bad_words(update, context):
    await update.message.reply_text("Получишь по губам и рукам!")

async def reply_money(update, context):
    await update.message.reply_text("Денег нет! Не было! И не будет!")

async def reply_understand(update, context):
    await update.message.reply_text("Точно понятно?! Или ещё несколько раз объяснить?")

async def reply_eat(update, context):
    await update.message.reply_text("На попе шерсть!")

async def reply_forward_or_link(update, context):
    await update.message.reply_text("А это точно тут нужно?")

# === Главный текстовый обработчик ===

async def handle_text(update, context):
    text = update.message.text
    if not text:
        return

    words_clean = text_to_words(text)
    text_lower = text.lower()

    # 1. Мат — высший приоритет
    if contains_bad_word(text):
        await reply_bad_words(update, context)
        return

    # 2. Слово "деньги"
    if 'деньги' in text_lower.split():
        await reply_money(update, context)
        return

    # 3. Слова "понял"/"поняла"
    if contains_understand_word(text):
        await reply_understand(update, context)
        return

    # 4. Слово "есть" (как отдельное слово)
    if contains_eat_word(text):
        await reply_eat(update, context)
        return

    # 5. Пересылки и ссылки
    if update.message.forward_date:
        await reply_forward_or_link(update, context)
        return

    if "http://" in text or "https://" in text:
        await reply_forward_or_link(update, context)
        return

# === Команды ===

async def start(update, context):
    await update.message.reply_text(
        "Привет! Я семейный помощник 🍬\n"
        "Фото → похвалю!\n"
        "Мат → по губам!\n"
        "«Деньги» → не будет!\n"
        "«Понял/поняла» → уточню!\n"
        "«Есть» → на попе шерсть!\n"
        "Ссылки/пересылки → «А это точно тут нужно?»"
    )

async def help_command(update, context):
    await update.message.reply_text(
        "Я реагирую на:\n"
        "📷 Фото → «Ты молодец! Держи конфетку!»\n"
        "🤬 Мат → «Получишь по губам и рукам!»\n"
        "💰 «Деньги» → «Денег нет! Не было! И не будет!»\n"
        "🧠 «Понял/Поняла» → «Точно понятно?! Или ещё несколько раз объяснить?»\n"
        "🍽️ «Есть» → «На попе шерсть!»\n"
        "🔁 Пересылки / 🔗 Ссылки → «А это точно тут нужно?»"
    )

# === Запуск ===

def main():
    token = os.getenv("BOT_TOKEN")
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO, reply_praise))
    app.add_handler(MessageHandler(filters.TEXT, handle_text))
    app.add_handler(MessageHandler(
        filters.FORWARDED & ~filters.PHOTO & ~filters.TEXT,
        reply_forward_or_link
    ))
    
    app.run_polling()

if __name__ == "__main__":
    main()
