# imports
import random
from datetime import datetime, timezone

import discord

# Date & Time
def format_value(value):
    if value is None:
        return "Not set"

    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")

    return str(value)

# All placeholders - configure as you like

def get_placeholders(
    member: discord.Member,
    channel: discord.TextChannel,
) -> dict[str, str]:

    guild = member.guild
    client = member._state._get_client()
    now = datetime.now().astimezone()
    now_utc = datetime.now(timezone.utc)

    owner = guild.owner
    top_role = member.top_role

    # Member roles, excluding @everyone
    roles = [role.mention for role in member.roles if role != guild.default_role]
    roles_text = ", ".join(roles) if roles else "No roles"

    # Member activities
    activities = getattr(member, "activities", [])
    activity_names = [activity.name for activity in activities if activity.name]
    activity_text = ", ".join(activity_names) if activity_names else "No activity"

    # Member status and device information
    status = str(getattr(member, "status", "unknown"))
    mobile = getattr(member, "mobile_status", None)
    desktop = getattr(member, "desktop_status", None)
    web = getattr(member, "web_status", None)

    # Current member count
    member_count = guild.member_count or len(guild.members)

    # Channel category
    category = channel.category

    placeholders = {
        # Member
        "user": member.mention,
        "user.mention": member.mention,
        "user.name": member.name,
        "user.display_name": member.display_name,
        "user.global_name": member.global_name or member.name,
        "user.id": str(member.id),
        "user.tag": str(member),
        "user.avatar": member.display_avatar.url,
        "user.default_avatar": member.default_avatar.url,
        "user.created_at": format_value(member.created_at),
        "user.created_at_timestamp": str(int(member.created_at.timestamp())),
        "user.is_bot": str(member.bot),
        "user.is_system": str(member.system),
        "user.nickname": member.nick or "No nickname",
        "user.color": str(member.color),
        "user.top_role": top_role.mention,
        "user.top_role.name": top_role.name,
        "user.top_role.mention": top_role.mention,
        "user.joined_at": format_value(member.joined_at),
        "user.joined_at_timestamp": (
            str(int(member.joined_at.timestamp()))
            if member.joined_at else "Not set"
        ),
        "user.boosting": str(member.premium_since is not None),
        "user.boost_since": format_value(member.premium_since),
        "user.pending": str(getattr(member, "pending", False)),
        "user.roles": roles_text,
        "user.roles_count": str(max(len(member.roles) - 1, 0)),
        "user.status": status,
        "user.activity": activity_text,
        "user.activities": activity_text,
        "user.is_mobile": str(mobile == discord.Status.online),
        "user.is_desktop": str(desktop == discord.Status.online),
        "user.is_web": str(web == discord.Status.online),

        # Server
        "server": guild.name,
        "server.name": guild.name,
        "server.id": str(guild.id),
        "server.icon": guild.icon.url if guild.icon else "No icon",
        "server.banner": guild.banner.url if guild.banner else "No banner",
        "server.splash": guild.splash.url if guild.splash else "No splash",
        "server.description": guild.description or "No description",
        "server.owner": owner.mention if owner else "Unknown",
        "server.owner.name": owner.name if owner else "Unknown",
        "server.owner.id": str(owner.id) if owner else "Unknown",
        "server.created_at": format_value(guild.created_at),
        "server.created_at_timestamp": str(int(guild.created_at.timestamp())),
        "server.member_count": str(member_count),
        "server.members_count": str(member_count),
        "server.boost_count": str(guild.premium_subscription_count or 0),
        "server.boost_level": str(guild.premium_tier),
        "server.verification_level": str(guild.verification_level),
        "server.explicit_content_filter": str(guild.explicit_content_filter),
        "server.features": ", ".join(guild.features) or "No features",
        "server.roles_count": str(len(guild.roles)),
        "server.channels_count": str(len(guild.channels)),
        "server.text_channels_count": str(len(guild.text_channels)),
        "server.voice_channels_count": str(len(guild.voice_channels)),
        "server.categories_count": str(len(guild.categories)),
        "server.emojis_count": str(len(guild.emojis)),
        "server.stickers_count": str(len(guild.stickers)),

        # Channel
        "channel": channel.mention,
        "channel.name": channel.name,
        "channel.id": str(channel.id),
        "channel.mention": channel.mention,
        "channel.category": category.name if category else "No category",
        "channel.category_id": str(category.id) if category else "Not set",
        "channel.topic": channel.topic or "No topic",

        # Date and time
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "year": str(now.year),
        "month": str(now.month),
        "month_name": now.strftime("%B"),
        "day": str(now.day),
        "weekday": now.strftime("%A"),
        "hour": str(now.hour),
        "minute": str(now.minute),
        "second": str(now.second),
        "unix_timestamp": str(int(now.timestamp())),
        "utc_date": now_utc.strftime("%Y-%m-%d"),
        "utc_time": now_utc.strftime("%H:%M:%S"),

        # Bot
        "bot": client.user.mention,
        "bot.name": client.user.name,
        "bot.id": str(client.user.id),
        "bot.avatar": client.user.display_avatar.url,
        "bot.created_at": format_value(client.user.created_at),
        "bot.latency": str(round(client.latency * 1000)),
        "bot.guilds_count": str(len(client.guilds)),
        "bot.users_count": str(len(client.users)),

        # Extra
        "member_number": str(member_count),
        "random_number": str(random.randint(1, 100)),
    }

    return placeholders


def replace_placeholders(
    text: str,
    member: discord.Member,
    channel: discord.TextChannel,
) -> str:

    placeholders = get_placeholders(member, channel)

    for name, value in placeholders.items():
        text = text.replace("{" + name + "}", value)

    return text
