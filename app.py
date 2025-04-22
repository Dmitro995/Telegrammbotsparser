import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler
from trends_parser import run_parser

TOKEN = "7543116655:AAE1nd4PfNQGLSCloQDBkqy40-DWBI_8mU4"
WEBHOOK_URL = f"https://telegrammbotsparser.onrender.com/{TOKEN}"

bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=1, use_context=True)

def check(update, context):
    update.message.reply_text("🔍 Checking for new trends...")
    try:
        new_items = run_parser()
        if new_items:
            message = "🆕 New Casino Trends:\n\n" + "\n".join(f"- {item}" for item in new_items)
        else:
            message = "No new trends found."
    except Exception as e:
        message = f"Error: {str(e)}"
    update.message.reply_text(message)

dispatcher.add_handler(CommandHandler("check", check))

@app.route("/" + TOKEN, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "Bot is running via webhook."

if __name__ == "__main__":
    bot.set_webhook(WEBHOOK_URL)
    app.run(host="0.0.0.0", port=5000)
