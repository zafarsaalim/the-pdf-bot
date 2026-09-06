import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
USDT_TRC_ADDRESS = os.environ.get("USDT_TRC_ADDRESS")
USDT_TOKEN_ID = os.environ.get("USDT_TOKEN_ID")
USDT_PAYMENT_LINK = os.environ.get("USDT_PAYMENT_LINK")
USDT_TRC_ADDRESS = os.environ.get("USDT_TRC_ADDRESS")

PRICING_TIERS = [
    (5, 10),    # 1–5 pages = 10 USDT
    (10, 20),   # 6–10 pages = 20 USDT
    (float('inf'), 30)  # >10 pages = 30 USDT
]



