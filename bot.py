import logging
from telegram.ext import Updater, CommandHandler
from trends_parser import run_parser
import json

with open("config.json") as f:
    config = json.load(f)

TOKEN = config["telegram_bot_token"]
CHAT_ID = config["telegram_chat_id"]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def check(update, context):
    update.message.reply_text("🔍 Checking for new trends...")
    new_items = run_parser()
    if new_items:
        message = "🎰 New Casino Trends:\n" + "\n".join(f"- {item}" for item in new_items)
        message = message.replace("\n", "
")
    else:
        message = "No new trends found."
    update.message.reply_text(message)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("check", check))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()