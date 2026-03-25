from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

COMICS_PATH = DATA_DIR / "comics.json"
PERSONAJES_PATH = DATA_DIR / "personajes.json"

ITEMS_PER_PAGE = 10
REQUEST_TIMEOUT = 20

COMICVINE_API_KEY = os.getenv("COMICVINE_API_KEY", "")
COMICVINE_BASE_URL = "https://comicvine.gamespot.com/api"


def validate_config():
    DATA_DIR.mkdir(exist_ok=True)

    if not COMICS_PATH.exists():
        COMICS_PATH.write_text("[]", encoding="utf-8")

    if not PERSONAJES_PATH.exists():
        PERSONAJES_PATH.write_text("[]", encoding="utf-8")

    if not COMICVINE_API_KEY:
        raise ValueError("Falta COMICVINE_API_KEY en el archivo .env")