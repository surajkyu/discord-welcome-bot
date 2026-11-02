# imports
import discord
from discord import app_commands
import json

from .groups import welcome_group
from .placeholders import replace_placeholders

# new class
class save_embed_view(discord.ui.View):
    def __init__(self, guild_id: int, embed_json: str):
        super().__init__(timeout=180)

        self.guild_id = guild_id
        self.embed_json = embed_json

    # /welcome embed button configuration

    @discord.ui.button( 
        label="Save embed",
        style=discord.ButtonStyle.success
    )
    async def save_embed(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        # make sure the button click immediately
        await interaction.response.defer()

        # postgresql query - update embed_json in the database
        try:
            result = await interaction.client.db.execute(
                """
                UPDATE welcome_settings
                SET embed_json = $1::jsonb
                WHERE guild_id = $2
                """,
                self.embed_json,
                self.guild_id
            )
            
            # some error handling

            if result == "UPDATE 0":
                await interaction.edit_original_response(
                    content="❌ No welcome settings found. Configure the welcome channel first.",
                    view=self
                )
                return

            button.disabled = True

            await interaction.edit_original_response(
                content="✅ Embed saved for this server!",
                view=self
            )

        except Exception as error:
            print(f"Failed to save embed: {error}")

            await interaction.edit_original_response(
                content=f"❌ Couldn't save the embed: `{error}`",
                view=self
            )


def replace_in_value(value, member, channel):
    if isinstance(value, str):
        return replace_placeholders(value, member, channel)

    if isinstance(value, list):
        return [
            replace_in_value(item, member, channel)
            for item in value
        ]

    if isinstance(value, dict):
        return {
            key: replace_in_value(item, member, channel)
            for key, item in value.items()
        }

    return value

# sub-command initiate
@app_commands.command(
    name="embed",
    description="Preview and save a welcome embed from a JSON file"
)
@app_commands.describe(file="The .json file (you can find the structure on the bot github wiki)")
# permissions check
@app_commands.checks.has_permissions(manage_guild=True)
async def embed_preview(
    interaction: discord.Interaction,
    file: discord.Attachment
):
    if not file.filename.lower().endswith(".json"):
        await interaction.response.send_message(
            "Please upload a `.json` file.",
            ephemeral=True
        )
        return

    file_content = await file.read()

    try:
        data = json.loads(file_content)
    except json.JSONDecodeError:
        await interaction.response.send_message(
            "That file doesn't contain valid JSON.",
            ephemeral=True
        )
        return

    if not isinstance(data, dict):
        await interaction.response.send_message(
            "The JSON file must contain an object.",
            ephemeral=True
        )
        return

    if "embeds" in data:
        embed_data = data["embeds"]
    else:
        embed_data = [data]

    if not isinstance(embed_data, list):
        await interaction.response.send_message(
            'Expected an embed object or an object containing `"embeds"`.',
            ephemeral=True
        )
        return

    if not 1 <= len(embed_data) <= 10:
        await interaction.response.send_message(
            "Please provide between 1 and 10 embeds.",
            ephemeral=True
        )
        return

    # keep the original JSON for saving
    original_json = json.dumps(data)

    # use the command runner as the preview member
    member = interaction.user

    # Postgresql query - use the configured welcome channel for channel placeholders
    row = await interaction.client.db.fetchrow(
        """
        SELECT channel_id
        FROM welcome_settings
        WHERE guild_id = $1
        """,
        interaction.guild_id
    )

    if row is None:
        await interaction.response.send_message(
            "Please configure your welcome channel first.",
            ephemeral=True
        )
        return

    channel = interaction.guild.get_channel(row["channel_id"])

    if channel is None:
        await interaction.response.send_message(
            "The configured welcome channel could not be found.",
            ephemeral=True
        )
        return

    try:
        # replace placeholders in a copy for preview only.
        preview_embed_data = replace_in_value(
            embed_data,
            member,
            channel
        )

        embeds = [
            discord.Embed.from_dict(embed)
            for embed in preview_embed_data
        ]

        content = replace_placeholders(
            data.get("content", ""),
            member,
            channel
        )

    except (TypeError, ValueError, KeyError) as error:
        await interaction.response.send_message(
            f"Couldn't create the preview: `{error}`",
            ephemeral=True
        )
        return

    view = save_embed_view(
        interaction.guild_id,
        original_json
    )

    await interaction.response.send_message(
        content=content or "Embed preview:",
        embeds=embeds,
        view=view,
        ephemeral=True
    )


welcome_group.add_command(embed_preview)
