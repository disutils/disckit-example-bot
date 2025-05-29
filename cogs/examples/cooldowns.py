"""
This module defines commands to demonstrate the usage of the `CoolDown` utility.

Classes:
--------
- CooldownCommands: A cog containing commands to showcase cooldown functionality.

Functions:
----------
- setup(bot: Bot) -> None:
    Asynchronously adds the `CooldownCommands` cog to the bot instance.

Commands:
---------
- cooldown user: Demonstrates a user-specific cooldown.
- cooldown guild: Demonstrates a guild-specific cooldown.
- cooldown channel: Demonstrates a channel-specific cooldown.
- cooldown sku: Demonstrates a user-specific cooldown with SKU bypass.
- cooldown reset: Resets the cooldown for a specific command.
"""

from typing import override

from disckit.utils.cooldown import CoolDown, CoolDownBucket
from disckit.utils.embeds import ErrorEmbed, SuccessEmbed
from discord import Interaction, app_commands
from discord.ext import commands

from core import Bot


class CooldownCommands(commands.Cog, name="Cooldown Commands"):
    """
    A cog to demonstrate the usage of the `CoolDown` utility.

    This cog contains commands that showcase different types of cooldowns,
    including user-specific, guild-specific, channel-specific, and SKU-based cooldowns.
    It also includes a command to reset a specific cooldown.

    Attributes:
    -----------
    bot : Bot
        The bot instance to which this cog is attached.

    Methods:
    --------
    cooldown.user(interaction: Interaction) -> None:
        Demonstrates a user-specific cooldown of 10 seconds.

    cooldown.guild(interaction: Interaction) -> None:
        Demonstrates a guild-specific cooldown of 20 seconds.

    cooldown.channel(interaction: Interaction) -> None:
        Demonstrates a channel-specific cooldown of 15 seconds.

    cooldown.sku(interaction: Interaction) -> None:
        Demonstrates a user-specific cooldown of 30 seconds, bypassable with a specific SKU.

    cooldown.reset(interaction: Interaction) -> None:
        Resets the cooldown for the `user` command.
    """

    def __init__(self, bot: Bot) -> None:
        """
        Initializes the CooldownExamples cog.

        Parameters:
        -----------
        bot : Bot
            The bot instance to which this cog is attached.
        """
        self.bot = bot  # pyright: ignore[reportUnannotatedClassAttribute]

    @override
    async def cog_load(self) -> None:
        """
        Logs when the cog is loaded.
        """
        print(f"\033[94m{self.__class__.__name__} has been loaded.\033[0m")

    @override
    async def cog_unload(self) -> None:
        """
        Logs when the cog is unloaded.
        """
        print(f"\033[94m{self.__class__.__name__} has been unloaded.\033[0m")

    cooldown_cmds: app_commands.Group = app_commands.Group(
        name="cooldown",
        description="Commands to demonstrate cooldown functionality.",
        guild_only=True,
    )

    @cooldown_cmds.command(name="user")
    @CoolDown.cooldown(time=10, bucket_type=CoolDownBucket.USER)
    async def user_cooldown(self, interaction: Interaction) -> None:
        """
        A command with a user-specific cooldown of 10 seconds.

        Parameters:
        -----------
        interaction : Interaction
            The interaction that triggered this command.
        """
        await interaction.response.send_message(
            embed=SuccessEmbed(
                "User Cooldown",
                "This command is on a 10-second cooldown per user.",
            ),
            ephemeral=True,
        )

    @cooldown_cmds.command(name="guild")
    @CoolDown.cooldown(time=20, bucket_type=CoolDownBucket.GUILD)
    async def guild_cooldown(self, interaction: Interaction) -> None:
        """
        A command with a guild-specific cooldown of 20 seconds.

        Parameters:
        -----------
        interaction : Interaction
            The interaction that triggered this command.
        """
        await interaction.response.send_message(
            embed=SuccessEmbed(
                "Guild Cooldown",
                "This command is on a 20-second cooldown per guild.",
            ),
            ephemeral=True,
        )

    @cooldown_cmds.command(name="channel")
    @CoolDown.cooldown(time=15, bucket_type=CoolDownBucket.CHANNEL)
    async def channel_cooldown(self, interaction: Interaction) -> None:
        """
        A command with a channel-specific cooldown of 15 seconds.

        Parameters:
        -----------
        interaction : Interaction
            The interaction that triggered this command.
        """
        await interaction.response.send_message(
            embed=SuccessEmbed(
                "Channel Cooldown",
                "This command is on a 15-second cooldown per channel.",
            ),
            ephemeral=True,
        )

    @cooldown_cmds.command(name="sku")
    @CoolDown.cooldown(time=30, bucket_type=CoolDownBucket.USER, sku_id=12345)
    async def sku_cooldown(self, interaction: Interaction) -> None:
        """
        A command with a user-specific cooldown of 30 seconds, bypassable with a specific SKU.

        Parameters:
        -----------
        interaction : Interaction
            The interaction that triggered this command.
        """
        await interaction.response.send_message(
            embed=SuccessEmbed(
                "SKU Cooldown",
                "This command is on a 30-second cooldown per user, bypassable with SKU.",
            ),
            ephemeral=True,
        )

    @cooldown_cmds.command(name="reset")
    async def reset_cooldown(self, interaction: Interaction) -> None:
        """
        Resets the cooldown for the user on the `user` command.

        Parameters:
        -----------
        interaction : Interaction
            The interaction that triggered this command.
        """
        reset = CoolDown.reset(
            interaction, bucket_type=CoolDownBucket.USER, command_name="user"
        )
        if reset:
            await interaction.response.send_message(
                embed=SuccessEmbed(
                    "Cooldown Reset", "The cooldown for `user` has been reset."
                ),
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                embed=ErrorEmbed(
                    "Cooldown Reset Failed",
                    "No active cooldown found to reset.",
                ),
                ephemeral=True,
            )


async def setup(bot: Bot) -> None:
    """
    Adds the CooldownCommands cog to the bot.

    Parameters:
    -----------
    bot : Bot
        The bot instance to which the cog will be added.
    """
    await bot.add_cog(CooldownCommands(bot))
