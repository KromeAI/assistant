import os
import logging
import asyncio
import nest_asyncio
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Autoriser asyncio dans l'environnement
nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)

# Vérification des variables d’environnement
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not OPENAI_API_KEY or not TELEGRAM_TOKEN:
    raise RuntimeError("Les variables OPENAI_API_KEY et TELEGRAM_TOKEN doivent être définies.")

client = OpenAI(api_key=OPENAI_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_input}]
    )

    answer = response.choices[0].message.content.strip()
    await update.message.reply_text(answer)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot Render en ligne !")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
