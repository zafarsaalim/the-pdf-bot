
import os

# Render will supply BOT_TOKEN from Environment Variables.
# Locally, it will fall back to reading from a local .env file or environment variable.
BOT_TOKEN = os.environ.get("BOT_TOKEN")
