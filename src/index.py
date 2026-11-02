# imports
import discord
from discord.ext import commands
from src.database.db import create_pool

# intents
intents = discord.Intents.default()
intents.members = True

# fetch commands & database
class bot(commands.Bot):
    async def setup_hook(self):
        self.db = await create_pool()

        await self.load_extension("src.commands.welcome") # fetch all the command diles from `src/commands/welcome/`

        synced = await self.tree.sync() # commands sync
        print(f"Synced {len(synced)} slash commands")

    async def on_member_join(self, member: discord.Member): # member join event
        from src.commands.welcome.send_welcome import send_welcome

        await send_welcome(member)


client = bot(intents=intents)
