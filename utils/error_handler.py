# error_handler.py
import logging

# Configure logging (optional, only once in main)
#logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)
#import logging

# Keep bot console clean and safe
logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.WARNING)

def get_clean_error_handler():
    async def clean_error_handler(update: object, context):
        # Logs only the error type and message
        error = context.error
        logging.error(f"{type(error).__name__}: {error}")
    return clean_error_handler
