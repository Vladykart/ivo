from dotenv import load_dotenv
import pathlib
import os

ROOT_DIR = pathlib.Path.cwd()
LOCAL_DATA_PATH = ROOT_DIR.joinpath("data")

load_dotenv()

GOOGLE_ANALYTICS_CREDENTIALS = {
    "key_file_location": ROOT_DIR.joinpath(
        "spirit-api-339912-3c7dbfa1dc4b.json"
    ),
    "view_id": os.environ.get("VIEW_ID"),
}

LOGIN_CREDENTIALS = {
    'names': os.environ['NAMES'],
    'usernames': os.environ['USERNAMES'],
    'passwords': os.environ['PASSWORDS']
}

