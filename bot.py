import os
import threading
from flask import Flask
import telebot

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8805701033
CHANNEL_LINK = "https://t.me/your_channel_username"

bot = telebot.TeleBot(TOKEN)
app = Flask(name)


@app.route("/")
def home():
    return "Bot is running!", 200


@bot.message_handler(commands=["start"])
def start(message):
    welcome = (
        "👋 Welcome!\n\n"
        "Please join our channel first:\n"
        f"{CHANNEL_LINK}\n\n"
        "Then send your guess."
    )
    bot.reply_to(message, welcome)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user = message.from_user
    text = message.text

    bot.send_message(
        ADMIN_ID,
        f"👤 User: {user.first_name}\n"
        f"🆔 ID: {user.id}\n"
        f"💬 Message: {text}"
    )

    bot.reply_to(message, "✅ Your guess has been received!")


def run_web():
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


if name == "main":
    threading.Thread(target=run_web, daemon=True).start()
    print("Bot started successfully...")
    bot.infinity_polling()
