# import
import discord
from discord import app_commands

from .groups import channel_group

# initiate add sub-command - /welcome channel add - check src/commands/welcome/groups.py for main-command and sub-group
@app_commands.command(
    name="add",
    description="Add the welcome channel"
)
@app_commands.describe(channel="Add the welcome message channel here")
@app_commands.checks.has_permissions(manage_guild=True)
async def channel_add(
    interaction: discord.Interaction,
    channel: discord.TextChannel
):
    # Postgresql query

    await interaction.client.db.execute(
        """
        INSERT INTO welcome_settings (guild_id, channel_id)
        VALUES ($1, $2)
        ON CONFLICT (guild_id)
        DO UPDATE SET channel_id = EXCLUDED.channel_id
        """,
        interaction.guild_id,
        channel.id
    )

    await interaction.response.send_message(
        f"Welcome channel set to {channel.mention}",
        ephemeral=True
    )

channel_group.add_command(channel_add)
