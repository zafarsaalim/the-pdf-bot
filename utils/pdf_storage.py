import os
from datetime import datetime

async def ssave_pdf(user_id: str, feature: str, doc):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_folder = f"./records/{user_id}/{feature}/{timestamp}"
    os.makedirs(base_folder, exist_ok=True)
    file_path = os.path.join(base_folder, doc.file_name)
    tg_file = await doc.get_file()
    await tg_file.download_to_drive(file_path)
    return file_path


async def dsave_pdf(user_id: str, feature: str, doc):
    if feature == "merge":
        # Create a timestamped folder for each merge task
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        merge_folder = f"./records/{user_id}/merge/{timestamp}"
        os.makedirs(merge_folder, exist_ok=True)

        file_path = os.path.join(merge_folder, doc.file_name)
    else:
        # Other features (clean, split, etc.) remain unchanged
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_folder = f"./records/{user_id}/{feature}/{timestamp}"
        os.makedirs(base_folder, exist_ok=True)
        file_path = os.path.join(base_folder, doc.file_name)

    # Download the file to the specified path
    tg_file = await doc.get_file()
    await tg_file.download_to_drive(file_path)
    
    return file_path






async def rsave_pdf(user_id: str, feature: str, doc, context):
    if feature == "merge":
        # Check if 'merge_folder' already exists in context (which is shared across the session)
        if "merge_folder" not in context.chat_data:
            # Create a single folder for the entire merge task session
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            merge_folder = f"./records/{user_id}/merge/{timestamp}"
            os.makedirs(merge_folder, exist_ok=True)
            context.chat_data["merge_folder"] = merge_folder
        else:
            merge_folder = context.chat_data["merge_folder"]

        file_path = os.path.join(merge_folder, doc.file_name)
    else:
        # For other features (clean, split, etc.), continue as before
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_folder = f"./records/{user_id}/{feature}/{timestamp}"
        os.makedirs(base_folder, exist_ok=True)
        file_path = os.path.join(base_folder, doc.file_name)

    # Download the file to the specified path
    tg_file = await doc.get_file()
    await tg_file.download_to_drive(file_path)

    return file_path




async def tsave_pdf(user_id: str, feature: str, doc, context):
    if feature == "merge":
        # Create a new folder for every new merge session using timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        merge_folder = f"./records/{user_id}/merge/{timestamp}"
        os.makedirs(merge_folder, exist_ok=True)  # Create the folder for this merge session

        # Store the folder path in context.chat_data for this session
        context.chat_data["merge_folder"] = merge_folder

        file_path = os.path.join(merge_folder, doc.file_name)
    else:
        # For other features (clean, split, etc.), continue as before
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_folder = f"./records/{user_id}/{feature}/{timestamp}"
        os.makedirs(base_folder, exist_ok=True)
        file_path = os.path.join(base_folder, doc.file_name)

    # Download the file to the specified path
    tg_file = await doc.get_file()
    await tg_file.download_to_drive(file_path)

    return file_path




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
