# imports
import discord
from discord import app_commands

from .groups import channel_group

# initiate remove sub-command - /welcome channel remove - check src/commands/welcome/groups.py for main-command and sub-group
@app_commands.command(
    name="remove",
    description="Remove the configured welcome channel"
)
# permissions check
@app_commands.checks.has_permissions(manage_guild=True)
async def channel_remove(interaction: discord.Interaction):

    # Postgresql query
    deleted_id = await interaction.client.db.fetchval(
        """
        DELETE FROM welcome_settings
        WHERE guild_id = $1
        RETURNING channel_id
        """,
        interaction.guild_id
    )
    
    # somewhat error handling
    if deleted_id is None:
        await interaction.response.send_message(
            "There is no welcome channel configured.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        "Welcome channel configuration removed.",
        ephemeral=True
    )


channel_group.add_command(channel_remove)
