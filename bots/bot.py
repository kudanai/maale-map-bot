# superclass for bot
from fastapi import FastAPI


class MapBot:
    """
    superclass for a MapBot instance
    """

    def __init__(self, datasource, token=None):
        self.data_source = datasource
        self.token = token

    async def setup_listener(self, app: FastAPI, host=None):
        pass

