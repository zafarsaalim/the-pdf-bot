
#import os

# Render will supply BOT_TOKEN from Environment Variables.
# Locally, it will fall back to reading from a local .env file or environment variable.
#BOT_TOKEN = os.environ.get("BOT_TOKEN")
import os

# Telegram Bot Token
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# USDT Address imported by metaclean.py
USDT_TRC_ADDRESS = os.environ.get("USDT_TRC_ADDRESS")

USDT_TOKEN_ID = os.environ.get("USDT_TOKEN_ID")
USDT_PAYMENT_LINK = os.environ.get("USDT_PAYMENT_LINK")

PRICING_TIERS = [
    (5, 15),    # 1–5 pages = 10 USDT
    (10, 25),   # 6–10 pages = 20 USDT
    (float('inf'), 30)  # >10 pages = 30 USDT
]
