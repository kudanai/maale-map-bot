from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineQuery, InlineQueryResultVenue, Message
from datasources import AddressSource, SQLiteDatasource
from settings import *


# initialize the bot
bot = Bot(token=MAPBOT_API_TOKEN)
dp = Dispatcher(bot)
data_source:AddressSource = SQLiteDatasource(SQLITE_SOURCE)

@dp.inline_handler()
async def inline_query_handler(inline_query: InlineQuery):
    q = inline_query.query
    results = [
                InlineQueryResultVenue(
                    id = x['id'],
                    latitude= x['latitude'],
                    longitude= x['longitude'],
                    title=x['title'],
                    address=x['address']
                ) for x in await data_source.get_addresses_results(q)
            ]
    await bot.answer_inline_query(inline_query.id, results=results, cache_time=1)


@dp.message_handler(commands=["start", "help"])
async def start_handler(message: Message):
    try:
        await message.answer(
            "Welcome to Male' Maps Bot. Type in the address you wish to search. You can also query this bot inline"
        )
    except Exception as e:
        pass


@dp.message_handler()
async def message_handler(message: Message):
    try:
        addresses = await data_source.get_addresses_results(message.text)
        address = addresses[0] if addresses else None   # pick one
        if address:
            await message.answer_venue(
                address["latitude"],
                address["longitude"],
                address["title"],
                address["address"]
            )
        else:
            suggestions = await data_source.get_suggestions(message.text)
            suggestions_flat = "\n".join([f"* {x}" for x in suggestions])
            await message.answer(
                "Sorry! Could not find the address\n" + 
                ("Did you mean:\n\n" + f"{suggestions_flat}" if suggestions else "")
            )
    except Exception as e:
        pass

async def on_startup(dp):
    await bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}")


async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == '__main__':
    
    if WEBHOOK:
        executor.start_webhook(
            dp, 
            WEBHOOK_PATH, 
            on_startup=on_startup, 
            on_shutdown=on_shutdown, 
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT)
    else: 
        executor.start_polling(dp, skip_updates=True)