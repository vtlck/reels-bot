import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Пришли ссылку на Reels — я скачаю его для тебя 📥")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com/reel" not in url:
        await update.message.reply_text("Это не ссылка на Reels. Попробуй снова.")
        return

    try:
        api_url = "https://saveig.app/api/ajaxSearch"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"q": url}
        r = requests.post(api_url, data=data, headers=headers)
        video_url = r.json()["data"][0]["url"]
        await update.message.reply_video(video=video_url)
    except Exception as e:
        await update.message.reply_text("Ошибка при скачивании видео 😔")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.run_polling()
