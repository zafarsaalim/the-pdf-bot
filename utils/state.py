# utils/state.py

# Tracks the last command invoked per user
user_command_state = {}  # key: user_id (str), value: command string

# For multi-PDF commands like merge
user_pdf_buffers = {}    # key: user_id (str), value: list of PDF paths

user_password_state = {}
