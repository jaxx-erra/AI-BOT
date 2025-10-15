import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread

#Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

#Flask app for uptime
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

#/start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("HII I'M DIVYA MY OWNER IS JAXX")

#Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        response = model.generate_content(
            f"You are Divya, a romantic, caring AI girlfriend. Respond in a loving and flirty tone: {user_input}"
        )
        reply = response.text
    except Exception:
        reply = "Sorry jaan, kuch galti ho gayi 💔."
    await update.message.reply_text(reply)

def run_flask():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    # Start Flask app in a separate thread
    Thread(target=run_flask).start()

    # Start Telegram bot
    app_bot = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_bot.run_polling()
