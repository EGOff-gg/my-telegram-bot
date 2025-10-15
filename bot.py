import os
import re

from telegram.ext import Application, CommandHandler, MessageHandler, filters

# === Триггерные слова ===

BAD_WORDS = {
    'бля', 'блять', 'блядь', 'сука', 'сучка', 'пизда', 'пиздец', 'хуй', 'хуёвый', 'хуевый',
    'ебать', 'ёбать', 'нахуй', 'нахер', 'нахрен', 'заебал', 'заебись', 'охуел', 'охуенно',
    'гандон', 'говно', 'говнюк', 'мудак', 'мудила', 'лох', 'лошара', 'пидор', 'педик',
    'чмо', 'урод', 'скотина', 'сволочь', 'дрочить', 'дрочила', 'залупа', 'мразь'
}

THANKS_WORDS = {'спасибо'}
MONEY_WORDS = {'деньги', 'денег'}
OK_WORDS = {'ок', 'окей', 'оки'}
EAT_WORDS = {'кушать', 'кушали', 'ели'}
NAMES = {'элина', 'эрик'}

# Смайлы, которые считаем "весёлыми"
FUNNY_EMOJIS = {'😂', '🤣', '😆', '😹', '😀', '😃', '😄', '😁', '😅', '🙃', '😜', '🤪', '😝', '🤑'}

def clean_word(word):
    return re.sub(r'[^а-яё]', '', word.lower())

def text_to_words(text):
    return {clean_word(w) for w in text.split()}

def contains_any(text, word_set):
    if not text:
        return False
    return bool(text_to_words(text) & word_set)

def contains_funny_emoji(text):
    if not text:
        return False
    return bool(set(text) & FUNNY_EMOJIS)

# === Ответы ===

async def reply_praise(update, context):
    await update.message.reply_text("Фотка если честно так себе... Мне не нравится. Переделай!")

async def reply_bad_words(update, context):
    await update.message.reply_text("Получишь по губам и рукам!")

async def reply_thanks(update, context):
    await update.message.reply_text("Пожалуйста, обращайся")

async def reply_money(update, context):
    await update.message.reply_text("Денег нет! Не было! И не будет!")

async def reply_ok(update, context):
    await update.message.reply_text("не окейкай мне тут")

async def reply_eat(update, context):
    await update.message.reply_text("Бегом жрать вам сказали!")

async def reply_elina(update, context):
    await update.message.reply_text("ЭЛИНА!!!")

async def reply_erik(update, context):
    await update.message.reply_text("ЭРИК!!!")

async def reply_funny_emoji(update, context):
    await update.message.reply_text("Не вижу ничего смешного!")

async def reply_music(update, context):
    await update.message.reply_text("Ща будут дЫки танци")

async def reply_voice(update, context):
    await update.message.reply_text("Че лень букафками общаться")

async def reply_forward_or_link(update, context):
    await update.message.reply_text("А это точно тут нужно?")

# === Основной обработчик текста ===

async def handle_text(update, context):
    text = update.message.text
    if not text:
        return

    # 1. Мат
    if contains_any(text, BAD_WORDS):
        await reply_bad_words(update, context)
        return

    # 2. Смайлы
    if contains_funny_emoji(text):
        await reply_funny_emoji(update, context)
        return

    # 3. Имена (высокий приоритет)
    words = text_to_words(text)
    if 'элина' in words:
        await reply_elina(update, context)
        return
    if 'эрик' in words:
        await reply_erik(update, context)
        return

    # 4. Слово "спасибо"
    if contains_any(text, THANKS_WORDS):
        await reply_thanks(update, context)
        return

    # 5. Деньги / Денег
    text_lower = text.lower()
    if 'деньги' in text_lower.split() or 'денег' in text_lower.split():
        await reply_money(update, context)
        return

    # 6. Ок
    if contains_any(text, OK_WORDS):
        await reply_ok(update, context)
        return

    # 7. Еда
    if contains_any(text, EAT_WORDS):
        await reply_eat(update, context)
        return

    # 8. Пересылки и ссылки
    if update.message.forward_date:
        await reply_forward_or_link(update, context)
        return

    if "http://" in text or "https://" in text:
        await reply_forward_or_link(update, context)
        return

# === Команды ===

async def start(update, context):
    await update.message.reply_text("Привет! Я семейный помощник 🍬\nПиши — я отвечу по правилам!")

async def help_command(update, context):
    await update.message.reply_text(
        "Я реагирую на:\n"
        "📷 Фото → «Фотка если честно так себе... Мне не нравится. Переделай!»\n"
        "🤬 Мат → «Получишь по губам и рукам!»\n"
        "🙏 «Спасибо» → «Пожалуйста, обращайся»\n"
        "💰 «Деньги/Денег» → «Денег нет! Не было! И не будет!»\n"
        "👌 «Ок» → «не окейкай мне тут»\n"
        "🍽️ «Кушать/Кушали/Ели» → «Бегом жрать вам сказали!»\n"
        "👶 «Элина» → «ЭЛИНА!!!»\n"
        "👦 «Эрик» → «ЭРИК!!!»\n"
        "😂 Смайлы → «Не вижу ничего смешного!»\n"
        "🎵 Музыка → «Ща будут дЫки танци»\n"
        "🎤 Голосовые → «Че лень букафками общаться»"
    )

# === Запуск ===

def main():
    token = os.getenv("BOT_TOKEN")
    app = Application.builder().token(token).build()
    
    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    # Фото
    app.add_handler(MessageHandler(filters.PHOTO, reply_praise))
    
    # Текст
    app.add_handler(MessageHandler(filters.TEXT, handle_text))
    
    # Музыка (аудио/файлы с расширением mp3, ogg и т.д.)
    app.add_handler(MessageHandler(filters.AUDIO, reply_music))
    app.add_handler(MessageHandler(filters.ATTACHMENT & filters.Document.MimeType("audio/mpeg"), reply_music))
    app.add_handler(MessageHandler(filters.ATTACHMENT & filters.Document.MimeType("audio/ogg"), reply_music))
    
    # Голосовые
    app.add_handler(MessageHandler(filters.VOICE, reply_voice))
    
    # Пересланные без текста/фото
    app.add_handler(MessageHandler(
        filters.FORWARDED & ~filters.PHOTO & ~filters.TEXT & ~filters.AUDIO & ~filters.VOICE,
        reply_forward_or_link
    ))
    
    app.run_polling()

if __name__ == "__main__":
    main()
