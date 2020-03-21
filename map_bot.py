from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineQuery, InlineQueryResultVenue
from datasources import AddressSource, SQLiteDatasource, PandasDatasource
from settings import MAPBOT_API_TOKEN, USE_CSV, DEBUG, SQLITE_SOURCE, CSV_SOURCE


# initialize the bot
bot = Bot(token=MAPBOT_API_TOKEN)
dp = Dispatcher(bot)
data_source:AddressSource = PandasDatasource(CSV_SOURCE) if USE_CSV else SQLiteDatasource(SQLITE_SOURCE)

@dp.inline_handler()
async def address_query_handler(inline_query: InlineQuery):
    q = inline_query.query
    results = await data_source.get_addresses_results(q)
    await bot.answer_inline_query(inline_query.id, results=results, cache_time=1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)