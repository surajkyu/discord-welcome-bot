# imports
import discord
import json
from .placeholders import replace_placeholders


async def send_welcome(member: discord.Member):
    client = member._state._get_client()

    # Postgresql query - fetch the channel and embed message from the database per guild
    row = await client.db.fetchrow(
        """
        SELECT channel_id, embed_json
        FROM welcome_settings
        WHERE guild_id = $1
        """,
        member.guild.id
    )

    if row is None:
        return

    channel = member.guild.get_channel(row["channel_id"])
    data = row["embed_json"]

    if channel is None or not data:
        return

    # PostgreSQL may return JSONB as a string
    if isinstance(data, str):
        data = json.loads(data)

    # Replace placeholders in message content
    content = data.get("content", "")
    content = replace_placeholders(content, member, channel)

    # Replace placeholders inside embed JSON too
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
