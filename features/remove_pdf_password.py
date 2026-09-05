import os
import subprocess
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from utils.animations import show_spinner
from utils.payment import get_usdt_payment_button
from utils.pricing import get_pdf_price

from utils.state import user_command_state  # <- add here with other imports

async def remove_pdf_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pdf_path = context.chat_data.get("original_pdf")
    if not pdf_path or not os.path.exists(pdf_path):
        await update.message.reply_text("No PDF uploaded yet. Send a PDF first.")
        return
    password = update.message.text.strip()
    status_msg = await update.message.reply_text("Removing password protection…")
    spinner_task = asyncio.create_task(show_spinner(status_msg, "Removing"))
    base, ext = os.path.splitext(pdf_path)
    unprotected_path = f"{base}_nopass{ext}"
    try:
        subprocess.run(
            ["qpdf", f"--password={password}", "--decrypt", pdf_path, unprotected_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        spinner_task.cancel()
        await status_msg.edit_text("🔓 Password protection removed successfully!")
        await asyncio.sleep(0.3)
        await status_msg.reply_document(open(unprotected_path, "rb"))
        await asyncio.sleep(1.2)
        await update.message.reply_text(
            f"💰 If you like QuickMate, you can support us (optional):",
            reply_markup=get_usdt_payment_button()
        )

    except subprocess.CalledProcessError as e:
        spinner_task.cancel()
        err_msg = e.stderr.decode() if e.stderr else str(e)
        await status_msg.edit_text(f"❌ Failed to remove password protection:\n{err_msg}")

    finally:
        user_id = str(update.message.from_user.id)
        user_command_state.pop(user_id, None)

