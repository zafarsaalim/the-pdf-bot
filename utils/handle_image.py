import io

async def handle_image(update):
    if update.message.photo:
        file = await update.message.photo[-1].get_file()
        file_name = "photo.jpg"
    elif update.message.document and update.message.document.mime_type.startswith("image"):
        file = await update.message.document.get_file()
        file_name = update.message.document.file_name
    else:
        await update.message.reply_text("❌ Send a valid image file.")
        return None, None

    data = await file.download_as_bytearray()
    return io.BytesIO(data)
