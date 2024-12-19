from dotenv import load_dotenv
from os import getenv, path
from cryptography.fernet import Fernet
from common.LogDataModel import LogData
from datetime import datetime

def write_log(user, event, message):
    load_dotenv()
    encryption_key = getenv("ENCRYPTION_KEY")
    encrypter = Fernet(encryption_key)
    time = datetime.now()
    reformatted_hour = f"{time.hour}" if len(f"{time.hour}") > 1 else f"0{time.hour}"
    reformatted_minute = f"{time.minute}" if len(f"{time.minute}") > 1 else f"0{time.minute}"
    reformatted_second = f"{time.second}" if len(f"{time.second}") > 1 else f"0{time.second}"
    reformatted_time = f"{reformatted_hour}:{reformatted_minute}:{reformatted_second} {time.day}-{time.month}-{time.year}"
    log_data = f"{user},{event},{message},{reformatted_time}"

    encrypted_text = encrypter.encrypt(log_data.encode()).decode() + "\n"

    current_directory = path.dirname(__file__).split("\\")
    file_path = ("\\".join(current_directory[:len(current_directory) - 1])) + "\\Logs\\logs.txt"

    with open(file_path, "a") as file:

        file.writelines(encrypted_text)

def get_logs():
    load_dotenv()
    encryption_key = getenv("ENCRYPTION_KEY")
    encrypter = Fernet(encryption_key)

    current_directory = path.dirname(__file__).split("\\")
    file_path = ("\\".join(current_directory[:len(current_directory) - 1])) + "\\Logs\\logs.txt"

    if not path.isfile(file_path):
        with open(file_path, "w"): # set up blank log file if one does not exist
            pass

    lines = []
    decrypted_lines = []
    with open(file_path, "r") as file:
        for line in file:
            lines.append(line)

    for line in lines:
        decrypted_line = encrypter.decrypt(line).decode()
        categories = decrypted_line.split(",")

        decrypted_lines.append(LogData(categories[0], categories[1], categories[2], categories[3]))

    return decrypted_lines[::-1] # reverse so that logs are displayed most recent first