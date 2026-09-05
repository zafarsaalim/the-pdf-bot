# commands/image_to_pdf.py
import os
import subprocess
from telegram import Update
from telegram.ext import ContextTypes
from utils.handle_image import handle_image
from utils.state import user_command_state
from datetime import datetime
async def handle_img2pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_command_state.get(user_id) != "img2pdf":
        return
    await update.message.reply_text("⏳ Converting your image to PDF…")
    img_bytes = await handle_image(update)
    if not img_bytes:
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    user_folder = f"./records/{user_id}/img2pdf/{timestamp}"
    os.makedirs(user_folder, exist_ok=True)
    if update.message.document:
        img_path = os.path.join(user_folder, update.message.document.file_name)
    else:  # Photo
        img_path = os.path.join(user_folder, f"photo.jpg")  # or any default name
    with open(img_path, "wb") as f:
        f.write(img_bytes.getvalue())

    pdf_path = os.path.join(user_folder, f"{os.path.splitext(os.path.basename(img_path))[0]}.pdf")
    for cmd in ["magick", "convert"]:
        try:
            subprocess.run([cmd, img_path, pdf_path], check=True)
            break
        except FileNotFoundError:
            continue
        except subprocess.CalledProcessError:
            continue
    else:
        await update.message.reply_text("❌ PDF conversion failed. Make sure ImageMagick is installed.")
        return
    await update.message.reply_document(
        open(pdf_path, "rb"),
        filename=os.path.basename(pdf_path),
        caption="✅ Here is your PDF!"
    )
    user_command_state[user_id] = None

