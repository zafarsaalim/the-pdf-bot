from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import USDT_TRC_ADDRESS, USDT_TOKEN_ID

def get_usdt_payment_button():
    payment_link = f"https://link.trustwallet.com/send?coin=195&address={USDT_TRC_ADDRESS}&token_id={USDT_TOKEN_ID}"
    keyboard = [
        [InlineKeyboardButton("💰 Support QuickMate (USDT, optional)", url=payment_link)]
    ]
    return InlineKeyboardMarkup(keyboard)
