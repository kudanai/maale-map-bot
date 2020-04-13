import json
import subprocess

from fastapi import FastAPI, Request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import (
    TextMessage,
    LocationMessage
)
from viberbot.api.messages.data_types.location import Location
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest

from bots import MapBot
from settings import *


class ViberBot(MapBot):

    def __init__(self, data_source, token):
        super(ViberBot, self).__init__(data_source, token)
        self.app = FastAPI()
        self.bot = Api(BotConfiguration(
            name='malemapbot',
            avatar='https://drive.google.com/uc?id=1h2gAJtlWd9o1yyXqU6l19kXKPIsizDp9',
            auth_token=self.token
        ))
        self.init_bot()

    def init_bot(self):
        bot = self.bot
        data_source = self.data_source
        app = self.app

        @app.post("/")
        async def handle_request(request: Request):

            # this library supplies a simple way to receive a request object
            data = await request.json()
            message = json.dumps(data).encode("utf-8")

            # if not bot.verify_signature(message, request.headers.get('X-Viber-Content-Signature')):
            #     return Response(status_code=403)

            r = bot.parse_request(message)

            try:

                if isinstance(r, ViberMessageRequest):
                    query = r.message.text
                    addresses = data_source.get_addresses_results(query)
                    address = next((x for x in addresses if x['title'].lower() == query.lower()), None)

                    if address:
                        message = LocationMessage(location=Location(
                            lat=address["latitude"],
                            lon=address["longitude"]
                        ))
                    else:
                        suggestions = data_source.get_suggestions(query)
                        suggestions_flat = "\n".join([f"* {x}" for x in suggestions])
                        message = TextMessage(text=
                                              "Sorry! Could not find the address\n" +
                                              ("Did you mean:\n\n" + f"{suggestions_flat}" if suggestions else "")
                                              )

                    bot.send_messages(r.sender.id, [message])

                elif isinstance(r, ViberSubscribedRequest):
                    bot.send_messages(r.user.id, [
                        TextMessage(text="thanks for subscribing!")
                    ])
                elif isinstance(r, ViberFailedRequest):
                    pass

                return Response(status_code=200)

            except Exception as e:
                print(e)
                return Response(status_code=200)

    @staticmethod
    def set_hook_extern(hook):
        try:
            bot = Api(BotConfiguration(
                name='malemapbot',
                avatar='https://drive.google.com/uc?id=1h2gAJtlWd9o1yyXqU6l19kXKPIsizDp9',
                auth_token=MAPBOT_API_TOKEN_VIBER
            ))
            bot.set_webhook(hook)
        except Exception as e:
            print(e)

    async def setup_listener(self, app: FastAPI, host=None):
        hook_path = f"{WEBHOOK_PATH}/viber/process/"
        app.mount(hook_path, self.app)

        hooker = f"{host}{hook_path}"

        # mother fucking viber. This is the sort of shit that makes people hate you
        subprocess.Popen(["python", "-c", f"from bots import ViberBot;from time import sleep; sleep(10);ViberBot.set_hook_extern('{hooker}')"])


