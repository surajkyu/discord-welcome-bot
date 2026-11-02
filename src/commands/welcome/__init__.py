# imports (imp) - to add new commands create a new file and add the name of that file in here - current setup is for welcome command
from .groups import welcome_group
from . import channel_add, channel_show, channel_remove, embed_preview, test

async def setup(client):
    client.tree.add_command(welcome_group)
