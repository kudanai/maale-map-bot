from bots.bot import MapBot
from fastapi import FastAPI
from fastapi.responses import JSONResponse


class APIBot(MapBot):

    def __init__(self, data_source, token):
        super(APIBot, self).__init__(data_source, token)
        self.app = FastAPI()
        self.init_bot()

    def init_bot(self):
        """
        setups up the bot dispatcher and binds methods to it
        """
        app = self.app
        data_source = self.data_source

        @app.get("/")
        async def handle_response(q:str = "test"):
            response = {
                "matches": [],
                "suggestions": []
            }

            if q:
                response["matches"] = data_source.get_addresses_results(q)
                if not response["matches"]:
                    response["suggestions"] = data_source.get_suggestions(q)

            return JSONResponse(response)

    async def setup_listener(self, app: FastAPI, host=None):
        app.mount("/api", self.app)
