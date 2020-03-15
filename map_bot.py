from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineQuery, InlineQueryResultVenue
from datasources import AddressSource, SQLiteDatasource, PandasDatasource
from dotenv import load_dotenv
import os

load_dotenv()

# initialize the bot
bot = Bot(token=os.getenv('MAPBOT_API_TOKEN'))
dp = Dispatcher(bot)

# set the bot data source.
data_source:AddressSource = PandasDatasource() if os.getenv('USE_CSV', "false") == "true" else SQLiteDatasource()

if os.getenv('DEBUG', default="false") == "true":
    import logging
    logging.basicConfig(level=logging.DEBUG)


@dp.inline_handler()
async def address_query_handler(inline_query: InlineQuery):
    q = inline_query.query
    await bot.answer_inline_query(inline_query.id, results=data_source.get_addresses_results(q), cache_time=1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)