from dotenv import load_dotenv
import pathlib
import os

ROOT_DIR = pathlib.Path.cwd()
LOCAL_DATA_PATH = ROOT_DIR.joinpath("data")

load_dotenv()


AGRID_OPTIONSS = {
    "fit_columns_on_grid_load": True,
    "allow_unsafe_jscode": True,
    "enable_enterprise_modules": True,
    "height": 500,
    "rows": 40,
}

VIEW_ID = os.environ.get("VIEW_ID"),


LOGIN_CREDENTIALS = {
    "names": os.environ["NAMES"],
    "usernames": os.environ["USERNAMES"],
    "passwords": os.environ["PASSWORDS"],
}

GOOGLE_KEY = {
    "type": os.environ.get("type"),
    "project_id": os.environ.get("project_id"),
    "private_key_id": os.environ.get("private_key_id"),
    "private_key": os.environ.get("private_key"),
    "client_email": os.environ.get("client_email"),
    "client_id": os.environ.get("client_id"),
    "auth_uri": os.environ.get("auth_uri"),
    "token_uri": os.environ.get("token_uri"),
    "auth_provider_x509_cert_url": os.environ.get("auth_provider_x509_cert_url"),
    "client_x509_cert_url": os.environ.get("client_x509_cert_url"),
}
print(os.environ.get("type"))
