import os
from datetime import datetime

async def save_image(user_id: str, feature: str, file_name: str, file_obj):
    """
    Saves image file (BytesIO or telegram file bytes)
    into: records/<user_id>/<feature>/<timestamp>/<file_name>
    Returns: full saved path
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_folder = f"./records/{user_id}/{feature}/{timestamp}"
    os.makedirs(base_folder, exist_ok=True)

    saved_path = os.path.join(base_folder, file_name)

    with open(saved_path, "wb") as f:
        f.write(file_obj.getvalue())   # file_obj is BytesIO

    return saved_path
