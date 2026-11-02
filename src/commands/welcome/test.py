#imports
import discord
import json
from discord import app_commands

from .groups import welcome_group
from .placeholders import replace_placeholders

# test welcome message command
@welcome_group.command(
    name="test",
    description="Test the welcome message"
)
async def welcome_test(interaction: discord.Interaction):
    # postgresql query - fetch the channel and embed message from database
    row = await interaction.client.db.fetchrow(
        """
        SELECT channel_id, embed_json
        FROM welcome_settings
        WHERE guild_id = $1
        """,
        interaction.guild_id
    )

    if row is None:
        await interaction.response.send_message(
            "Welcome settings haven't been configured yet.",
            ephemeral=True
        )
        return

    channel = interaction.guild.get_channel(row["channel_id"])
    data = row["embed_json"]

    if channel is None:
        await interaction.response.send_message(
            "The configured welcome channel could not be found.",
            ephemeral=True
        )
        return

    if not data:
        await interaction.response.send_message(
            "No welcome message has been saved yet.",
            ephemeral=True
        )
        return

    # PostgreSQL may return JSONB as a string
    if isinstance(data, str):
        data = json.loads(data)

    # who wants to be the test subject :) - defaukt to the person who runs the command
    member = interaction.user

    content = data.get("content", "")
    content = replace_placeholders(content, member, channel)

    embed_data_list = data.get("embeds", [])

    def replace_in_value(value):
        if isinstance(value, str):
            return replace_placeholders(value, member, channel)

        if isinstance(value, list):
            return [replace_in_value(item) for item in value]

        if isinstance(value, dict):
            return {
                key: replace_in_value(item)
                for key, item in value.items()
            }

        return value

    embed_data_list = replace_in_value(embed_data_list)

    embeds = [
        discord.Embed.from_dict(embed_data)
        for embed_data in embed_data_list
    ]

    await channel.send(
        content=content or None,
        embeds=embeds,
        allowed_mentions=discord.AllowedMentions(users=True)
    )

    await interaction.response.send_message(
        f"Test welcome message sent to {channel.mention}.",
        ephemeral=True
    )
