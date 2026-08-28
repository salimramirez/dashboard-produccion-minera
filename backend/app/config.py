import os

from dotenv import load_dotenv

load_dotenv()

GOLDAPI_TOKEN = os.getenv("GOLDAPI_TOKEN", "")
GOLDAPI_URL = "https://www.goldapi.io/api"
TIMEOUT_SEGUNDOS = 5.0
