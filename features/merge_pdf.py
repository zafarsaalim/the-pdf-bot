import subprocess
import tempfile
import os

async def ahandle_pdf_merge(file_list):
    out_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    out_file.close()
    cmd = ["pdfcpu", "merge", out_file.name] + file_list

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())
        raise Exception("Merge failed")
    return out_file.name


#import subprocess

async def shandle_pdf_merge(context):
    # Get the timestamped folder (stored in chat_data)
    merge_folder = context.chat_data["merge_folder"]
    merge_files = context.chat_data["merge_files"]

    # Output merged PDF file in the same timestamped folder
    out_file = os.path.join(merge_folder, "merged_output.pdf")

    # Command to merge PDFs using pdfcpu
    cmd = ["pdfcpu", "merge", out_file] + merge_files

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())
        raise Exception("Merge failed")

    return out_file



import subprocess
import os

async def handle_pdf_merge(file_list, context):
    # Get the merge folder from chat_data (stored in context)
    merge_folder = context.chat_data["merge_folder"]

    # Ensure the merged PDF is saved in the merge folder.
    out_file = os.path.join(merge_folder, "merged_output.pdf")

    # Command to merge PDFs using pdfcpu
    cmd = ["pdfcpu", "merge", out_file] + file_list

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())
        raise Exception("Merge failed")

    return out_file
