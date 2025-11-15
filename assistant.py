import os
import asyncio
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# -----------------------------
# Load environment variables
# -----------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

client = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------------
# OpenAI Chat Function
# -----------------------------
async def chat_with_openai(user_message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un assistant utile, amical, intelligent."},
                {"role": "user", "content": user_message},
            ]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"❌ Erreur OpenAI : {e}"

# -----------------------------
# Commands
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello ! Je suis ton assistant Telegram.")

# -----------------------------
# Main conversation handler
# -----------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    reply = await chat_with_openai(user_message)
    await update.message.reply_text(reply)

# -----------------------------
# MAIN
# -----------------------------
async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot Telegram lancé !")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
