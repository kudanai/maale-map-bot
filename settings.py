from dotenv import load_dotenv
import os

load_dotenv()

MAPBOT_API_TOKEN=os.getenv("MAPBOT_API_TOKEN")
USE_CSV=os.getenv('USE_CSV', "false") == "true"
DEBUG=os.getenv('DEBUG', "false") == "true"
CSV_SOURCE=os.getenv('CSV_SOURCE', os.path.join("databases", "male-map.csv"))
SQLITE_SOURCE=os.getenv("SQLITE_SOURCE", os.path.join("databases", "maalemap.db"))

WEBHOOK=os.getenv('WEBHOOK', "false") == "true"
WEBHOOK_PORT=int(os.getenv('WEBHOOK_PORT', "8001"))
WEBHOOK_URL=os.getenv('WEBHOOK_URL', "http://kudanai.xyz")
WEBHOOK_PATH=os.getenv('WEBHOOK_PATH', "/maalemaps/bot")

if DEBUG:
    import logging
    logging.basicConfig(level=logging.DEBUG)