import os
from datetime import datetime

async def save_pdf(user_id: str, feature: str, doc, context):
    if feature == "merge":
        print("savepdf")
        # Check if 'merge_folder' already exists in context (session folder)
        if "merge_folder" not in context.chat_data:
            # Create a unique folder for the session using timestamp (first file upload)
            session_folder_name = datetime.now().strftime("%Y%m%d_%H%M%S")
            merge_folder = f"./records/{user_id}/merge/{session_folder_name}"
            os.makedirs(merge_folder, exist_ok=True)

            # Store the session folder path in context for the entire session
            context.chat_data["merge_folder"] = merge_folder
        else:
            # Use the existing session folder for all files in this merge task
            merge_folder = context.chat_data["merge_folder"]

        # Save the uploaded file in the session folder
        file_path = os.path.join(merge_folder, doc.file_name)

    else:
        # For other tasks (clean, split, etc.), use timestamp as before
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_folder = f"./records/{user_id}/{feature}/{timestamp}"
        os.makedirs(base_folder, exist_ok=True)
        file_path = os.path.join(base_folder, doc.file_name)

    # Download the file to the specified path
    tg_file = await doc.get_file()
    await tg_file.download_to_drive(file_path)

    return file_path
