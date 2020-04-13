from bots import MapBot
from discord.ext import commands
from settings import *
from fastapi import FastAPI



class DiscordBot(MapBot):

	def __init__(self, data_source, token):
		super(DiscordBot, self).__init__(data_source, token)
		self.bot = commands.Bot(command_prefix="!")

	def init_bot(self):
		bot = self.bot
		data_source = self.data_source

		@bot.command()
		async def get_address(ctx, *, args):
			addresses = await data_source.get_addresses_results(args)
			address = next((x for x in addresses if x['title'].lower() == args.lower()), None)

			if address:
				msg = f"**{address['title']} {address['address']}**\nhttps://www.google.com/maps/place/{address['latitude']},{address['longitude']}"
				await ctx.send(msg)
			else:
				suggestions = await data_source.get_suggestions(args)
				suggestions_flat = "\n".join([f"* {x}" for x in suggestions])
				msg = "Sorry! Could not find the address\n" + ("Did you mean:**\n\n" + f"{suggestions_flat}" if suggestions else "") + "**"
				await ctx.send(msg)

	def setup_listener(self, app: FastAPI, host=None):
		self.bot.run(self.token)