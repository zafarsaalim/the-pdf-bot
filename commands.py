import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

from utils.handle_pdf import handle_pdf
from utils.error_handler import get_clean_error_handler
from utils.messages import START_MESSAGE
from utils.handle_text import handle_text
from utils.state import user_command_state

from features.qr_code import qr_generate 
from features.image_to_pdf import handle_img2pdf
from features.merge_pdf import handle_pdf_merge

from features.redact_pdf import redact_pdf #new redact

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_MESSAGE)


async def clean_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_command_state[str(update.message.from_user.id)] = "clean"
    await update.message.reply_text("Send the PDF you want to clean.")


async def split_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_command_state[str(update.message.from_user.id)] = "split"
    await update.message.reply_text("Send the PDF you want to split.")


async def remove_pass_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    user_command_state[user_id] = "remove_pass_wait_pdf"
    await update.message.reply_text("Send the PDF whose password you want to remove.")


async def qr_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_command_state[str(update.message.from_user.id)] = "qr"
    print("qr action")
    await update.message.reply_text("Send the text or link you want to convert into a QR code.")



#new redact 

async def redact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    user_command_state[user_id] = "redact_waiting_pdf"
    await update.message.reply_text("📁 Please upload the PDF file you want to redact.")

async def merge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_command_state[user_id] = "merge_waiting_files"
    context.chat_data["merge_files"] = []
    await update.message.reply_text(
        "📎 Send me the PDFs one-by-one in the order you want.\n"
        "When you're done, send /done")


async def done_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    active = user_command_state.get(user_id)
    if active != "merge_waiting_files":
        return await update.message.reply_text("❗ You're not merging right now.")
    files = context.chat_data.get("merge_files", [])
    if len(files) < 2:
        return await update.message.reply_text("❗ Send at least 2 PDFs to merge.")
    await update.message.reply_text("⏳ Merging files… please wait…")
    #merge update
    out_path = await handle_pdf_merge(files, context)
    await update.message.reply_document(
        document=open(out_path, "rb"),
        filename="merged.pdf")
    user_command_state[user_id] = None
    context.chat_data["merge_files"] = []
    #plus
    if "merge_folder" in context.chat_data:
        del context.chat_data["merge_folder"]

async def cut_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_command_state[user_id] = "cut_waiting_pdf"
    context.chat_data["cut_pdf"] = None
    await update.message.reply_text(
        "✂️ Send me the PDF you want to cut.\n"
        "After sending it, send text like:\n\n"
        "`2 3`\n(rows columns)\n",
        parse_mode="Markdown")


async def img2pdf_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sets state and prompts user to send an image."""
    user_id = update.effective_user.id
    user_command_state[user_id] = "img2pdf"
    await update.message.reply_text("📤 Send the image you want to convert to PDF.")



async def compress_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_command_state[user_id] = "compress_choose"

    keyboard = [
        ["Low", "Medium", "High"]
    ]

    await update.message.reply_text(
        "📦 Choose compression quality:",
        reply_markup={
            "keyboard": keyboard,
            "resize_keyboard": True,
            "one_time_keyboard": True
        }
    )




from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = [
    [
        InlineKeyboardButton("Low", callback_data="compress_low"),
        InlineKeyboardButton("Medium", callback_data="compress_medium"),
        InlineKeyboardButton("High", callback_data="compress_high")
    ]
]
markup = InlineKeyboardMarkup(keyboard)


async def xcompress_command(update, context):
    user_id = str(update.message.from_user.id)
    user_command_state[user_id] = "compress_choose"

    rkeyboard = [
        ["Low", "Medium", "High"]
    ]

    mrarkup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        "📦 Choose compression quality:",
        reply_markup=markup
    )
