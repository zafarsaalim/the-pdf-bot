import os
import asyncio
import fitz  # PyMuPDF
from telegram import Update
from telegram.ext import ContextTypes
from utils.animations import show_spinner
from utils.payment import get_usdt_payment_button
from utils.state import user_command_state

async def redact_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #user_id = str(update.message.from_user.id)
    pdf_path = context.chat_data.get("original_pdf")
    
    if not pdf_path or not os.path.exists(pdf_path):
        await update.message.reply_text("No PDF uploaded yet. Send a PDF first.")
        #user_command_state.pop(user_id, None)
        return

    input_text = update.message.text.strip()
    search_texts = [t.strip() for t in input_text.split(",") if t.strip()]

    if not search_texts:
        await update.message.reply_text("Please provide at least one text to redact, separated by commas.")
        return

    status_msg = await update.message.reply_text("Redacting text from PDF…")
    spinner_task = asyncio.create_task(show_spinner(status_msg, "Redacting"))

    base, ext = os.path.splitext(pdf_path)
    redacted_path = f"{base}_redacted{ext}"

    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            for text in search_texts:
                rects = page.search_for(text)
                for rect in rects:
                    page.add_redact_annot(rect, fill=(0, 0, 0))  # Black box redaction
            page.apply_redactions()

        doc.save(redacted_path)
        doc.close()

        spinner_task.cancel()
        await status_msg.edit_text("🔒 Text redacted successfully!")
        await asyncio.sleep(0.3)
        await status_msg.reply_document(open(redacted_path, "rb"))
        await asyncio.sleep(1.2)
        await update.message.reply_text(
            f"💰 If you like QuickMate, you can support us (optional):",
            reply_markup=get_usdt_payment_button()
        )

    except Exception as e:
        spinner_task.cancel()
        await status_msg.edit_text(f"❌ Failed to redact PDF text:\n{str(e)}")

    finally:
        user_id = str(update.message.from_user.id)
        user_command_state.pop(user_id, None)
