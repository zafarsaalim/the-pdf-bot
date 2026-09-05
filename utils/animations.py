# utils/animations.py
import asyncio

async def show_spinner(msg, text="Processing", duration=2):
    """
    Animate a message (msg: telegram.Message) with a spinner/dots
    Runs for 'duration' seconds.
    """
    spinner = ["", ".", "..", "..."]

    end_time = asyncio.get_event_loop().time() + duration
    i = 0
    while asyncio.get_event_loop().time() < end_time:
        await msg.edit_text(f"{text}{spinner[i % len(spinner)]}")
        i += 1
        await asyncio.sleep(0.25)

    return msg
