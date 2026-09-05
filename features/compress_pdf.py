# features/compress_pdf.py
import os
import subprocess
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from utils.animations import show_spinner
from utils.state import user_command_state
from utils.payment import get_usdt_payment_button


async def compress_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pdf_path = context.chat_data.get("original_pdf")

    if not pdf_path or not os.path.exists(pdf_path):
        await update.message.reply_text("❗ No PDF found. Send the PDF again.")
        return

    status_msg = await update.message.reply_text("📦 Compressing your PDF…")
    spinner_task = asyncio.create_task(show_spinner(status_msg, "Compressing"))

    # Output file
    base = os.path.splitext(pdf_path)[0]
    output_path = f"{base}_compressed.pdf"

    # Ghostscript compression command
    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",     # balanced compression
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        pdf_path
    ]

    try:
        subprocess.run(cmd, check=True)

        spinner_task.cancel()
        await status_msg.edit_text("✨ Compression complete!")

        with open(output_path, "rb") as f:
            await status_msg.reply_document(f, filename=os.path.basename(output_path))

        await update.message.reply_text(
            "💰 Support QuickMate (optional):",
            reply_markup=get_usdt_payment_button()
        )

    except subprocess.CalledProcessError:
        spinner_task.cancel()
        await status_msg.edit_text("❌ Compression failed. Try again.")

    finally:
        user_id = str(update.message.from_user.id)
        user_command_state.pop(user_id, None)
