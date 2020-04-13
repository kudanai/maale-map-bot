from fastapi import FastAPI, Request
from bots.bot import MapBot
from settings import *
import logging
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, MessageHandler, Filters
from telegram import InlineQueryResultVenue, Update


class TGBot(MapBot):

    def __init__(self, data_source, token):
        super(TGBot, self).__init__(data_source, token)
        self.updater = Updater(token=token, use_context=True)
        self.app = FastAPI()
        self.init_bot()

    def init_bot(self):
        """
        setups up the bot dispatcher and binds methods to it
        """

        updater = self.updater
        data_source = self.data_source
        app = self.app

        def inline_query_handler(update, context):
            logging.log(logging.DEBUG, "inline query")
            try:
                q = update.inline_query.query
                results = [
                    InlineQueryResultVenue(
                        id=x['id'],
                        latitude=x['latitude'],
                        longitude=x['longitude'],
                        title=x['title'],
                        address=x['address']
                    ) for x in self.data_source.get_addresses_results(q)
                ]

                context.bot.answer_inline_query(
                    update.inline_query.id,
                    results=results
                )
            except Exception as e:
                pass

        def start_handler(update, context):
            logging.log(logging.DEBUG, "new user")

            try:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Welcome to Male' Maps Bot. Type in the address you wish to search. You can also query this bot inline"
                )
            except Exception as e:
                pass

        def message_handler(update, context):
            logging.log(logging.DEBUG, "message")

            try:
                addresses = data_source.get_addresses_results(update.message.text)
                address = next((x for x in addresses if x['title'].lower() == update.message.text.lower()), None)

                if address:
                    context.bot.send_venue(
                        chat_id=update.effective_chat.id,
                        latitude=address["latitude"],
                        longitude=address["longitude"],
                        title=address["title"],
                        address=address["address"]
                    )
                else:
                    suggestions = data_source.get_suggestions(update.message.text)
                    suggestions_flat = "\n".join([f"* {x}" for x in suggestions])
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Sorry! Could not find the address\n" +
                             ("Did you mean:\n\n" + f"{suggestions_flat}" if suggestions else "")
                    )
            except Exception as e:
                pass

        @app.post(f"/")
        async def handle_request(request: Request):
            try:
                data = await request.json()
                update = Update.de_json(data, updater.bot)
                updater.dispatcher.process_update(update)
            except Exception as e:
                pass

        updater.dispatcher.add_handler(CommandHandler('start', start_handler))
        updater.dispatcher.add_handler(CommandHandler('help', start_handler))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
        updater.dispatcher.add_handler(InlineQueryHandler(inline_query_handler))

    async def setup_listener(self, app: FastAPI, host=None):
        hook_path = f"{WEBHOOK_PATH}/telegram/process/"
        app.mount(hook_path, self.app)
        self.updater.bot.set_webhook(f"{host}{hook_path}")
