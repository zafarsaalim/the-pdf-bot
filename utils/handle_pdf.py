import os
from telegram import Update
from telegram.ext import ContextTypes
from .handle_file import size_guard
from .state import user_command_state
from utils.pdf_storage import save_pdf

from features.metaclean import clean_pdf
from features.split_pdf import split_pdf
from features.remove_pdf_password import remove_pdf_password
from features.handle_pdf_cut import handle_pdf_cut
from features.compress_pdf import compress_pdf
from features.redact_pdf import redact_pdf #redact


async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await size_guard(update):
        return

    doc = update.message.document
    if doc.mime_type != "application/pdf":
        return await update.message.reply_text("Please send PDF only.")

    user_id = str(update.message.from_user.id)
    active_command = user_command_state.get(user_id)

    if not active_command:
        return await update.message.reply_text(
            "Please choose a command first:\n/clean /split /remove_pass /merge /cut"
        )

    # Map state → folder name for saving
    feature_map = {
        "clean": "clean",
        "split": "split",
        "merge_waiting_files": "merge",
        "remove_pass_wait_pdf": "remove_pass",
        "remove_pass_wait_password": "remove_pass",
        "cut_waiting_pdf": "cut",
        "compress_low": "compress",
        "compress_medium": "compress",
        "compress_high": "compress",
        "redact_waiting_pdf": "redact",
        "redact_waiting_text": "redact"
    }

    feature = feature_map.get(active_command, "other")

    saved_path = await save_pdf(user_id, feature, doc, context)

    context.chat_data["original_pdf"] = saved_path
    context.chat_data["current_pdf"] = saved_path

    if active_command == "clean":
        await update.message.reply_text("🧹 Cleaning PDF…")
        return await clean_pdf(update, context)
   
        # REDACT → first get PDF
    elif active_command == "redact_waiting_pdf":
        user_command_state[user_id] = "redact_waiting_text"
        return await update.message.reply_text(
            "✅ PDF received!\nNow send the text you want to redact (separate multiple terms with commas, e.g., `confidential, secret`)."
        )

    # REDACT → now user sends text
    elif active_command == "redact_waiting_text":
        return await redact_pdf(update, context)


    # SPLIT
    elif active_command == "split":
        await update.message.reply_text("✂️ Splitting PDF…")
        return await split_pdf(update, context)

    # REMOVE PASSWORD → first get PDF
    elif active_command == "remove_pass_wait_pdf":
        user_command_state[user_id] = "remove_pass_wait_password"
        return await update.message.reply_text("PDF received. Now send the password.")

    # REMOVE PASSWORD → now user sends password
    elif active_command == "remove_pass_wait_password":
        return await remove_pdf_password(update, context)

    elif active_command in ["compress_low", "compress_medium", "compress_high"]:
        return await compress_pdf(update, context)


    # MERGE MULTIPLE FILES
    elif active_command == "merge_waiting_files":
        #plus merge
        #
        context.chat_data.setdefault("merge_files", []).append(saved_path)
        count = len(context.chat_data["merge_files"])
        return await update.message.reply_text(
            f"📄 Added file {count}. Send more or type /done"
        )

    # CUT PDF (1st step)
    elif active_command == "cut_waiting_pdf":
        context.chat_data["cut_pdf"] = saved_path
        user_command_state[user_id] = "cut_waiting_xy"
        return await update.message.reply_text(
            "✔ PDF received!\nNow send rows and columns like: `2 2`",
            parse_mode="Markdown"
        )

    else:
        return await update.message.reply_text(
            "Invalid state. Please choose a command again."
        )
