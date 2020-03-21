from dotenv import load_dotenv
import os

load_dotenv()

MAPBOT_API_TOKEN=os.getenv("MAPBOT_API_TOKEN")
USE_CSV=os.getenv('USE_CSV', "false") == "true"
DEBUG=os.getenv('DEBUG', "false") == "true"
CSV_SOURCE=os.getenv('CSV_SOURCE', os.path.join("databases", "male-map.csv"))
SQLITE_SOURCE=os.getenv("SQLITE_SOURCE", os.path.join("databases", "maalemap.db"))


if DEBUG:
    import logging
    logging.basicConfig(level=logging.DEBUG)