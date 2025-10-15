import os
from telegram.ext import Application, MessageHandler, filters

async def handle_photo(update, context):
    """Реагирует на фото (включая отправленные и пересланные)"""
    await update.message.reply_text("Ты молодец! Держи конфетку!")

async def handle_forward_or_link(update, context):
    """Реагирует на пересланные сообщения или сообщения со ссылками"""
    # Проверяем, есть ли пересылка
    if update.message.forward_date:
        await update.message.reply_text("А это точно тут нужно?")
        return
    
    # Проверяем, есть ли ссылки в тексте
    if update.message.text:
        text = update.message.text
        if "http://" in text or "https://" in text:
            await update.message.reply_text("А это точно тут нужно?")
            return

async def ignore_other(update, context):
    """Игнорировать всё остальное (необязательно, но чисто)"""
    pass

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не установлен!")
    
    app = Application.builder().token(token).build()
    
    # Обработчик фото (включая документы-изображения)
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # Обработчик пересылок и ссылок
    app.add_handler(MessageHandler(
        filters.FORWARDED | filters.Entity("url") | filters.Entity("text_link"),
        handle_forward_or_link
    ))
    
    # Обработчик текста со ссылками (на случай, если ссылка не распознана как entity)
    app.add_handler(MessageHandler(filters.TEXT, handle_forward_or_link))
    
    # Запуск
    app.run_polling()

if __name__ == "__main__":
    main()
