from settings import *
from bots import TGBot, APIBot, ViberBot
from models import SQLiteDatasource
from fastapi import FastAPI
import asyncio
import uvicorn

app = FastAPI()
ds = SQLiteDatasource(SQLITE_SOURCE)


async def init():
    if DEBUG:
        import logging
        logging.basicConfig(level=logging.DEBUG)

    # for debugging, using an NGROK process to localhost
    # from pyngrok import ngrok
    # WEBHOOK_URL = ngrok.connect(WEBAPP_PORT).replace("http", "https").rstrip("/")

    bots = [
        TGBot(ds, MAPBOT_API_TOKEN),
        APIBot(ds, None),
        ViberBot(ds, MAPBOT_API_TOKEN_VIBER),
        # DiscordBot(ds, DISCORD_TOKEN)
    ]

    for bot in bots:
        await bot.setup_listener(app, WEBHOOK_URL)


if __name__ == "__main__":
    asyncio.run(init())
    uvicorn.run(app, host=WEBAPP_HOST, port=WEBAPP_PORT )


