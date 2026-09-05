import os
import glob
import shutil
import tempfile
import subprocess
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from utils.animations import show_spinner
from utils.pricing import get_pdf_price
from utils.payment import get_usdt_payment_button
from utils.state import user_command_state
async def split_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pdf_path = context.chat_data.get("original_pdf")
    if not pdf_path or not os.path.exists(pdf_path):
        await update.message.reply_text("⚠️ No valid PDF found. Please upload a PDF first.")
        return

    status_msg = await update.message.reply_text("Splitting your PDF… ⏳")
    outdir = None
    zip_path = None
    try:
        outdir = tempfile.mkdtemp(prefix="split_")
        subprocess.run(
            ["pdfcpu", "split", pdf_path, outdir],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        produced = sorted(glob.glob(os.path.join(outdir, "*.pdf")))
        zip_path = outdir + ".zip"
        shutil.make_archive(outdir, "zip", outdir)
        await status_msg.edit_text(f"✨ Split complete! {len(produced)} pages processed. Sending ZIP…")
        with open(zip_path, "rb") as f:
            await update.message.reply_document(f)

        await update.message.reply_text(
            f"💰 If you like QuickMate, you can support us (optional):",
            reply_markup=get_usdt_payment_button()
        )

    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode() if e.stderr else str(e)
        await status_msg.edit_text(f"❌ Split failed:\n{stderr}")

    except Exception as e:
        await status_msg.edit_text(f"Unexpected error: {str(e)}")

    finally:
        user_id = str(update.message.from_user.id)
        user_command_state.pop(user_id, None)  
        try:
            if zip_path and os.path.exists(zip_path):
                os.remove(zip_path)
            if outdir and os.path.exists(outdir):
                shutil.rmtree(outdir)
        except Exception:
            pass
