import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
from config import BOT_TOKEN as TOKEN
from commands import *

async def main_async():
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Explicitly initialize and start the application to prevent ExtBot uninitialized crashes on Python 3.14
    await app.initialize()
    await app.start()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clean", clean_command))
    app.add_handler(CommandHandler("split", split_command))
    app.add_handler(CommandHandler("remove_pass", remove_pass_command))
    app.add_handler(CommandHandler("qr", qr_command))
    app.add_handler(CommandHandler("compress_pdf", compress_command))
    app.add_handler(CommandHandler("merge", merge_command))
    app.add_handler(CommandHandler("done", done_command))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CommandHandler("img2pdf", img2pdf_command))
    app.add_handler(CommandHandler("cut", cut_command))
    app.add_handler(CommandHandler("redact", redact_command)) #new redact
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_img2pdf))

    app.add_error_handler(get_clean_error_handler())
    print("QuickMate Bot running...")
    
    # Start polling manually via updater
    await app.updater.start_polling(bootstrap_retries=-1)
    
    # Keep the application running
    stop_signal = asyncio.Future()
    await stop_signal

def main():
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
