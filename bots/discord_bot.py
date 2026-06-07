from bots import MapBot
import discord
from discord.ext import commands
from settings import *
from fastapi import FastAPI
import asyncio
import uvloop

class DiscordBot(MapBot):

    def __init__(self, data_source, token):
        super(DiscordBot, self).__init__(data_source, token)
        self.bot = commands.Bot(command_prefix="!")

    def init_bot(self):
        bot = self.bot
        data_source = self.data_source

        @bot.event
        async def on_ready():
            print(f'{bot.user.name} has connected to Discord!')

        @bot.command(name='address')
        async def address(ctx, *, args):
            addresses = data_source.get_addresses_results(args)
            address = next((x for x in addresses if x['title'].lower() == args.lower()), None)

            if address:
                msg = f"**{address['title']} {address['address']}**\nhttps://www.google.com/maps/place/{address['latitude']},{address['longitude']}"
                await ctx.send(msg)
            else:
                suggestions = await data_source.get_suggestions(args)
                suggestions_flat = "\n".join([f"* {x}" for x in suggestions])
                msg = "Sorry! Could not find the address\n" + (
                    "Did you mean:**\n\n" + f"{suggestions_flat}" if suggestions else "") + "**"
                await ctx.send(msg)

    async def setup_listener(self, app: FastAPI, host=None, loop=None):

        @app.on_event("startup")
        async def app_startup():
            loop.run_until_complete(self.bot.start(self.token))


