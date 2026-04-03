import os
import anthropic
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Saya AI Assistant powered by Claude.\n"
        "Silakan tanya apa saja!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("⏳ Sedang memproses...")

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": user_message
            }]
        )
        reply = response.content[0].text
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN tidak ditemukan!")
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY tidak ditemukan!")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message
    ))
    print("✅ Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
