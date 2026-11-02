# imports
from discord import app_commands

# set the main-command and sub-group for the channel commands and other commands
welcome_group = app_commands.Group(
    name="welcome",
    description="Welcome system commands"
)

channel_group = app_commands.Group(
    name="channel",
    description="Manage the welcome channel"
)

welcome_group.add_command(channel_group)
