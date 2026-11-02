# imports
import discord
from discord import app_commands

from .groups import channel_group

# initiate remove sub-command - /welcome channel remove - check src/commands/welcome/groups.py for main-command and sub-group
@app_commands.command(
    name="show",
    description="Show the current welcome channel"
)
async def channel_show(interaction: discord.Interaction):

    # Postgresql query
    channel_id = await interaction.client.db.fetchval(
        "SELECT channel_id FROM welcome_settings WHERE guild_id = $1",
        interaction.guild_id
    )

    # somewhat error handling
    if channel_id is None:
        await interaction.response.send_message(
            "No welcome channel has been configured.",
            ephemeral=True
        )
        return

    channel = interaction.guild.get_channel(channel_id)

    # again somewhat error handling
    if channel is None:
        await interaction.response.send_message(
            "The configured welcome channel could not be found.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"Current welcome channel: {channel.mention}",
        ephemeral=True
    )


channel_group.add_command(channel_show)
