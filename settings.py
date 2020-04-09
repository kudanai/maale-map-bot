from dotenv import load_dotenv
import os

load_dotenv()

# bot config
MAPBOT_API_TOKEN=os.getenv("MAPBOT_API_TOKEN", None)
DEBUG=os.getenv('DEBUG', "false") == "true"

# data sources
SQLITE_SOURCE=os.getenv("SQLITE_SOURCE", os.path.join("databases", "maalemap.db"))

# webhook config
WEBHOOK=os.getenv('WEBHOOK', "false") == "true"
WEBHOOK_PORT=int(os.getenv('WEBHOOK_PORT', "8001"))
WEBHOOK_URL=os.getenv('WEBHOOK_URL', "http://kudanai.xyz")
WEBHOOK_PATH=os.getenv('WEBHOOK_PATH', "/maalemaps/bot")

if DEBUG:
    import logging
    logging.basicConfig(level=logging.DEBUG)