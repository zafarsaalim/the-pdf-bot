import os
import subprocess
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from utils.animations import show_spinner
from config import USDT_TRC_ADDRESS as address
from config import USDT_PAYMENT_LINK as payment_link
from utils.pricing import get_pdf_price
from utils.payment import get_usdt_payment_button

from utils.state import user_command_state


async def clean_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pdf_path = context.chat_data.get("original_pdf")
    if not pdf_path or not os.path.exists(pdf_path):
        await update.message.reply_text("No PDF uploaded yet. Send a PDF first.")
        return
    await asyncio.sleep(2)
    status_msg = await update.message.reply_text("Cleaning…")
    spinner_task = asyncio.create_task(show_spinner(status_msg, "Cleaning"))
    base, ext = os.path.splitext(pdf_path)
    cleaned_path = f"{base}_clean{ext}"

    try:
        subprocess.run(
            ["exiftool", "-all=", "-o", cleaned_path, pdf_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        subprocess.run(
           ["qpdf", "--linearize", "--replace-input", cleaned_path],

           check=True,
           stdout=subprocess.PIPE,
           stderr=subprocess.PIPE
        )
        await asyncio.sleep(1)
        spinner_task.cancel()
        await status_msg.edit_text(f"✨ Metadata successfully removed!\nHere’s your cleaned file.")
        await asyncio.sleep(0.5)

        with open(cleaned_path, "rb") as f:
            await status_msg.reply_document(f)

        await asyncio.sleep(1)
        await update.message.reply_text(
            f"💰 If you like QuickMate, you can support us (optional):",
            reply_markup=get_usdt_payment_button()
        )
    except subprocess.CalledProcessError as e:
        spinner_task.cancel()
        err_msg = e.stderr.decode() if e.stderr else str(e)
        await status_msg.edit_text(f"❌ Cleaning failed:\n{err_msg}")
    finally:
        user_id = str(update.message.from_user.id)
        user_command_state.pop(user_id, None)
