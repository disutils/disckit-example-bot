"""
This module defines commands related to embeds for the `EmbedCommands` cog.

Classes:
--------
- EmbedCommands: A cog containing commands related to embeds.

Functions:
----------
- setup(bot: Bot) -> None:
    Asynchronously adds the `EmbedCommands` cog to the bot instance.

Commands:
---------
- embed main-embed: Demonstrates a main embed.
- embed success-embed: Demonstrates a success embed.
- embed error-embed: Demonstrates an error embed.
"""

from typing import override

from disckit.utils.embeds import ErrorEmbed, MainEmbed, SuccessEmbed
from discord import Interaction, app_commands
from discord.ext import commands

from core import Bot


class EmbedCommands(commands.Cog, name="Embed Commands"):
    """
    A cog containing commands related to embeds.

    Attributes:
    -----------
    embed_cmds : app_commands.Group
        A command group for embed-related commands.

    Methods:
    --------
    main_embed(interaction: Interaction) -> None:
        Demonstrates a main embed.

    success_embed(interaction: Interaction) -> None:
        Demonstrates a success embed.

    error_embed(interaction: Interaction) -> None:
        Demonstrates an error embed.
    """

    def __init__(self, bot: Bot) -> None:
        self.bot = bot  # pyright: ignore[reportUnannotatedClassAttribute]

    @override
    async def cog_load(self) -> None:
        print(f"\033[94m{self.__class__.__name__} has been loaded.\033[0m")

    @override
    async def cog_unload(self) -> None:
        print(f"\033[94m{self.__class__.__name__} has been unloaded.\033[0m")

    embed_cmds: app_commands.Group = app_commands.Group(
        name="embed",
        description="Commands related to embeds.",
        guild_only=True,
    )

    @embed_cmds.command(name="main-embed")
    async def main_embed(self, interaction: Interaction) -> None:
        """
        An example of a main embed.

        Parameters:
        -----------
        interaction : Interaction
            The interaction that triggered this command.
        """
        embed = MainEmbed(
            "Main Embed Example",
            "This is an example of a main embed.",
        )
        embed.add_field(name="Field 1", value="This is the first field.")
        embed.add_field(name="Field 2", value="This is the second field.")
        await interaction.response.send_message(embed=embed)

    @embed_cmds.command(name="success-embed")
    async def success_embed(self, interaction: Interaction) -> None:
        """
        An example of a success embed.

        Parameters:
        -----------
        interaction : Interaction
            The interaction that triggered this command.
        """
        embed = SuccessEmbed(
            "Success Embed Example",
            "This is an example of a success embed.",
        )
        embed.add_field(name="Field 1", value="This is the first field.")
        embed.add_field(name="Field 2", value="This is the second field.")
        await interaction.response.send_message(embed=embed)

    @embed_cmds.command(name="error-embed")
    async def error_embed(self, interaction: Interaction) -> None:
        """
        An example of an error embed.

        Parameters:
        -----------
        interaction : Interaction
            The interaction that triggered this command.
        """
        embed = ErrorEmbed(
            "Error Embed Example",
            "This is an example of an error embed.",
        )
        embed.add_field(name="Field 1", value="This is the first field.")
        embed.add_field(name="Field 2", value="This is the second field.")
        await interaction.response.send_message(embed=embed)


async def setup(bot: Bot) -> None:
    """
    Asynchronously adds the `EmbedCommands` cog to the bot instance.

    Parameters:
    -----------
    bot : Bot
        The bot instance to add the cog to.
    """
    await bot.add_cog(EmbedCommands(bot))
