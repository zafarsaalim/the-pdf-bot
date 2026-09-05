import os
import asyncio
import subprocess
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from utils.animations import show_spinner
from utils.payment import get_usdt_payment_button
from utils.state import user_command_state


async def qr_generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = str(update.message.from_user.id)
    feature_folder = os.path.abspath(f"./records/{user_id}/qr")   # QR feature folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")          # timestamp for subfolder
    user_folder = os.path.join(feature_folder, timestamp)         # final folder for this QR generation
    os.makedirs(user_folder, exist_ok=True)
    status_msg = await update.message.reply_text("Generating QR…")
    spinner = asyncio.create_task(show_spinner(status_msg, "Generating"))
    try:
        png_path = os.path.join(user_folder, "qr.png")
        svg_path = os.path.join(user_folder, "qr.svg")
        # Generate PNG
        subprocess.run(["qrencode", "-s", "10", "-o", png_path, text], check=True)
        # Generate SVG
        subprocess.run(["qrencode", "-t", "SVG", "-o", svg_path, text], check=True)
        await asyncio.sleep(1)
        spinner.cancel()
        await status_msg.edit_text("✨ QR codes ready!")
        await update.message.reply_photo(open(png_path, "rb"))
        await update.message.reply_document(open(svg_path, "rb"))
        await update.message.reply_text(
            "💰 Support QuickMate (optional):",
            reply_markup=get_usdt_payment_button()
        )

    except Exception as e:
        spinner.cancel()
        await status_msg.edit_text(f"❌ Failed:\n{e}")

    finally:
        spinner.cancel()
        user_command_state.pop(user_id, None)
