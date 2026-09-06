
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



PROVIDER_TOKEN= "5775769170:LIVE:TG_Dk_E9leC8sPIHe0qBvjAkFQA"
MODE = "test"
USDT_TRC_ADDRESS = "TWoxYTnujNiKTZu4XiDHTkGche5uwPZoDe"


PRICING_TIERS = [
    (5, 10),    # 1–5 pages = 10 USDT
    (10, 20),   # 6–10 pages = 20 USDT
    (float('inf'), 30)  # >10 pages = 30 USDT
]


USDT_WALLET_ADDRESS = "TWoxYTnujNiKTZu4XiDHTkGche5uwPZoDe"
