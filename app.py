import os
import logging
import random
import time

from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackContext

from trends_parser import run_parser

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Bot token from env
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
bot = Bot(token=TOKEN)

# Flask app
app = Flask(__name__)

# Dispatcher
dispatcher = Dispatcher(bot, None, use_context=True)

def check(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    bot.send_message(chat_id, "🔍 Checking for new trends...")
    new_items = run_parser()
    if new_items:
        text = "🎰 New Casino Trends:
" + "
".join(f"- {{item}}" for item in new_items)
    else:
        text = "No new trends found."
    bot.send_message(chat_id, text)

dispatcher.add_handler(CommandHandler("check", check))

@app.route(f"/webhook/{{TOKEN}}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return "OK"

if __name__ == "__main__":
    APP_URL = os.environ["APP_URL"].rstrip("/")  # e.g. https://your-render-url
    webhook_url = f"{APP_URL}/webhook/{TOKEN}"
    bot.set_webhook(webhook_url)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
