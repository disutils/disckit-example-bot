import logging

import discord
from discord import Interaction
from disckit.cogs import BaseCog
from disckit.utils import (
    MainEmbed,
    get_or_fetch_channel,
    get_or_fetch_guild,
    get_or_fetch_user,
)
from discord import app_commands

from core import Bot

_logger: logging.Logger = logging.getLogger(__name__)


class FetchExamples(BaseCog, name="Fetch Examples"):
    """
    A cog that demonstrates the usage of get_or_fetch_guild, get_or_fetch_user, and get_or_fetch_channel.

    Attributes
    ----------
    bot : Bot
        The bot instance to which this cog is added.
    """

    def __init__(self, bot: Bot) -> None:
        """
        Initialize the `FetchExamples` cog.

        Parameters
        ----------
        bot : Bot
            The bot instance to which this cog is added.
        """
        super().__init__(logger=_logger)
        self.bot: Bot = bot

    fetch_cmds: app_commands.Group = app_commands.Group(
        name="fetch",
        description="Commands to fetch guilds, users, and channels.",
    )

    @fetch_cmds.command()
    async def guild(
        self, interaction: Interaction, guild_id: str
    ) -> None:
        """
        Fetch a guild by its ID.

        Parameters
        ----------
        interaction : Interaction
            The interaction object representing the command invocation.
        guild_id : str
            The ID of the guild to fetch.
        """
        await interaction.response.defer()
        guild_obj = await get_or_fetch_guild(self.bot, int(guild_id))
        print(f"Fetched guild object: {guild_obj}")  # Debug print
        if guild_obj:
            embed = MainEmbed(title="Guild Information")
            embed.add_field(name="Name", value=guild_obj.name, inline=False)
            embed.add_field(name="ID", value=guild_obj.id, inline=False)
            embed.add_field(
                name="Owner ID", value=guild_obj.owner_id, inline=False
            )
            embed.add_field(
                name="Member Count", value=guild_obj.member_count, inline=False
            )
            embed.add_field(
                name="Created At",
                value=f"<t:{int(guild_obj.created_at.timestamp())}>",
                inline=False,
            )
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(
                f"Guild with ID {guild_id} not found."
            )

    @fetch_cmds.command()
    async def user(
        self, interaction: Interaction, user_id: str
    ) -> None:
        """
        Fetch a user by their ID.

        Parameters
        ----------
        interaction : Interaction
            The interaction object representing the command invocation.
        user_id : str
            The ID of the user to fetch.
        """
        await interaction.response.defer()
        user_obj = await get_or_fetch_user(self.bot, int(user_id))
        print(f"Fetched user object: {user_obj}")  # Debug print
        if user_obj:
            embed = MainEmbed(title="User Information")
            embed.add_field(
                name="Username",
                value=f"{user_obj.name}#{user_obj.discriminator}",
                inline=False,
            )
            embed.add_field(name="ID", value=user_obj.id, inline=False)
            embed.add_field(name="Bot", value=user_obj.bot, inline=False)
            embed.add_field(
                name="Created At",
                value=f"<t:{int(user_obj.created_at.timestamp())}>",
                inline=False,
            )
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(
                f"User with ID {user_id} not found."
            )

    @fetch_cmds.command()
    async def channel(
        self, interaction: Interaction, channel_id: str
    ) -> None:
        """
        Fetch a channel by its ID.

        Parameters
        ----------
        interaction : Interaction
            The interaction object representing the command invocation.
        channel_id : str
            The ID of the channel to fetch.
        """
        await interaction.response.defer()
        channel_obj = await get_or_fetch_channel(self.bot, int(channel_id))
        print(f"Fetched channel object: {channel_obj}")  # Debug print
        if isinstance(channel_obj, discord.TextChannel) or isinstance(
            channel_obj, discord.VoiceChannel
        ):
            embed = MainEmbed(title="Channel Information")
            embed.add_field(name="Name", value=channel_obj.name, inline=False)
            embed.add_field(name="ID", value=channel_obj.id, inline=False)
            embed.add_field(name="Type", value=channel_obj.type, inline=False)
            embed.add_field(
                name="Guild ID", value=channel_obj.guild.id, inline=False
            )
            embed.add_field(
                name="Created At",
                value=f"<t:{int(channel_obj.created_at.timestamp())}>",
                inline=False,
            )
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(
                f"Channel with ID {channel_id} is not a valid text or voice channel."
            )


async def setup(bot: Bot) -> None:
    """
    Add the `FetchExamples` cog to the bot.

    Parameters
    ----------
    bot : Bot
        The bot instance to which the cog is added.
    """
    await bot.add_cog(FetchExamples(bot))
