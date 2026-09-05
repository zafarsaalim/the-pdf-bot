from telegram import Update
from telegram.ext import ContextTypes
from utils.state import user_command_state
from features.qr_code import qr_generate
from features.remove_pdf_password import remove_pdf_password
from features.handle_pdf_cut import handle_pdf_cut
from features.compress_pdf import compress_pdf
from features.redact_pdf import redact_pdf #redact


from telegram import ReplyKeyboardRemove

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    state = user_command_state.get(user_id)

    if state == "qr":
        await qr_generate(update, context)
        
    elif state == "redact_waiting_text":
        await redact_pdf(update, context)
        return


    elif state == "compress_choose":
        choice = update.message.text.lower()

        if choice == "low":
            user_command_state[user_id] = "compress_low"
        elif choice == "medium":
            user_command_state[user_id] = "compress_medium"
        elif choice == "high":
            user_command_state[user_id] = "compress_high"
        else:
            return await update.message.reply_text("Choose Low / Medium / High")

        return await update.message.reply_text(
        "📤 Now send the PDF to compress.",
        reply_markup=ReplyKeyboardRemove())

    elif state == "remove_pass_wait_password":
        await remove_pdf_password(update, context)
    elif state == "cut_waiting_xy":
        try:
            parts = update.message.text.strip().split()
            rows, cols = int(parts[0]), int(parts[1])
        except:
            return await update.message.reply_text(
                "❗ Invalid input. Send like: 2 3")
        input_pdf = context.chat_data.get("cut_pdf")
        await update.message.reply_text("⏳ Cutting your PDF… Please wait…")
        out_path = await handle_pdf_cut(input_pdf, rows, cols)
        if not out_path:
            return await update.message.reply_text("❗ Failed to cut PDF.")
        await update.message.reply_document(
            document=open(out_path, "rb"),
            filename="cut.pdf")
        user_command_state[user_id] = None
        context.chat_data["cut_pdf"] = None
        return
    else:
        await update.message.reply_text(
            "I didn't understand that. Please choose a command first:\n"
            "/clean /redact /split /remove_pass /merge /img2pdf /cut /qr")
