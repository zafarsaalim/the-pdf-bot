MAX_MB = 10
MAX_BYTES = MAX_MB * 1024 * 1024

async def size_guard(update, max_bytes: int = MAX_BYTES) -> bool:
    msg = update.message
    file_obj = (
        msg.document
        or msg.video
        or msg.audio
        or msg.voice
        or (msg.photo[-1] if msg.photo else None)
    )

    if not file_obj:
        return True  # Nothing to check
    print(f"[DEBUG] File size: {file_obj.file_size / 1024 / 1024:.2f} MB")

    # Size check
    if file_obj.file_size > max_bytes:
        await msg.reply_text(
            f"❌ File too large ({file_obj.file_size/1024/1024:.1f} MB).\n"
            f"Limit: {max_bytes/1024/1024:.0f} MB."
        )
        return False
    return True
