import os
from telegram.ext import Application, MessageHandler, filters

async def handle_photo(update, context):
    await update.message.reply_text("Ты молодец! Держи конфетку!")

async def handle_forward_or_link(update, context):
    # Проверка: пересланное сообщение?
    if update.message.forward_date:
        await update.message.reply_text("А это точно тут нужно?")
        return
    
    # Проверка: есть ли ссылка в тексте?
    if update.message.text:
        text = update.message.text
        if "http://" in text or "https://" in text:
            await update.message.reply_text("А это точно тут нужно?")
            return

def main():
    token = os.getenv("BOT_TOKEN")
    app = Application.builder().token(token).build()
    
    # Обработчик фото
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # Обработчик всего остального (для проверки пересылок и ссылок)
    app.add_handler(MessageHandler(filters.ALL, handle_forward_or_link))
    
    app.run_polling()

if __name__ == "__main__":
    main()
