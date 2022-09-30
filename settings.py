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
    "credentials": os.getenv("credentials"),
    "view_id": os.environ.get("VIEW_ID"),
}

LOGIN_CREDENTIALS = {
    'names': os.environ['NAMES'],
    'usernames': os.environ['USERNAMES'],
    'passwords': os.environ['PASSWORDS']
}

google_key = {
  "type": os.environ.get("type"),
  "project_id": os.environ.get("project_id"),
  "private_key_id": os.environ.get("private_key_id"),
  "private_key": os.environ.get("private_key"),
  "client_email": os.environ.get("client_email"),
  "client_id": os.environ.get("client_id"),
  "auth_uri": os.environ.get("auth_uri"),
  "token_uri": os.environ.get("token_uri"),
  "auth_provider_x509_cert_url": os.environ.get("auth_provider_x509_cert_url"),
  "client_x509_cert_url": os.environ.get("client_x509_cert_url")
}
print(os.environ.get("type"))

