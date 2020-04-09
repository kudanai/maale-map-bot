from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineQuery, InlineQueryResultVenue, Message
from datasources import AddressSource, SQLiteDatasource, PandasDatasource
from settings import MAPBOT_API_TOKEN, USE_CSV, DEBUG, SQLITE_SOURCE, CSV_SOURCE, WEBHOOK, WEBHOOK_PORT, WEBHOOK_URL, WEBHOOK_PATH


# initialize the bot
bot = Bot(token=MAPBOT_API_TOKEN)
dp = Dispatcher(bot)
data_source:AddressSource = PandasDatasource(CSV_SOURCE) if USE_CSV else SQLiteDatasource(SQLITE_SOURCE)

@dp.inline_handler()
async def inline_query_handler(inline_query: InlineQuery):
    q = inline_query.query
    results = await data_source.get_addresses_results(q)
    await bot.answer_inline_query(inline_query.id, results=results, cache_time=1)


@dp.message_handler(commands=["start", "help"])
async def start_handler(message: Message):
    await message.answer(
        "Welcome to Male' Maps Bot. Type in the address you wish to search. You can also query this bot inline"
    )


@dp.message_handler()
async def message_handler(message: Message):
    address = await data_source.get_address(message.text)
    if isinstance(address,dict):
        await message.answer_venue(
            address["latitude"],
            address["longitude"],
            address["title"],
            address["address"]
        )
    elif isinstance(address,list):
        await message.answer(
            "Sorry! Could not find the address.\nDid you mean: \n\n" +
            "\n".join([f"  * {x['title']}" for x in address])
        )
    else:
        await message.answer(
            "Sorry! Could not find the address"
        )


async def on_startup(dp):
    await bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}")


async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == '__main__':
    if WEBHOOK:
            executor.start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host="localhost",
            port=WEBHOOK_PORT,
        )
    else: 
        executor.start_polling(dp, skip_updates=True)