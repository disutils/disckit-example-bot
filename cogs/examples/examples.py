"""
This module defines the `Examples` cog for the Discord bot, showcasing various utilities provided by `disckit.utils`.

Classes:
--------
- Examples: A cog containing example commands for utilities like embeds, autocomplete, and decorators.

Functions:
----------
- setup(bot: Bot) -> None:
    Asynchronously adds the `Examples` cog to the bot instance.

Commands:
---------
- embed.main-embed: Demonstrates a main embed.
- embed.success-embed: Demonstrates a success embed.
- embed.error-embed: Demonstrates an error embed.
- autocomplete: Demonstrates the autocomplete utility.
- sku-check: Demonstrates the SKU check utility.
- disallow-bots: Demonstrates the disallow bots decorator.
- is-owner: Demonstrates the is_owner decorator.
"""

import logging
from typing import override

import discord
from disckit.utils import disallow_bots, is_owner, make_autocomplete, sku_check
from disckit.utils.embeds import ErrorEmbed, MainEmbed, SuccessEmbed
from discord import Interaction, app_commands
from discord.ext import commands

from core import Bot

logger = logging.getLogger(__name__)


class Examples(commands.Cog, name="Examples"):
    """
    A cog containing examples for all utilities in `disckit.utils`.

    Attributes:
    -----------
    bot : Bot
        The bot instance associated with this cog.

    Methods:
    --------
    cog_load() -> None:
        Called when the cog is loaded.

    cog_unload() -> None:
        Called when the cog is unloaded.

    embed_cmds.main_embed(interaction: Interaction) -> None:
        Demonstrates a main embed.

    embed_cmds.success_embed(interaction: Interaction) -> None:
        Demonstrates a success embed.

    embed_cmds.error_embed(interaction: Interaction) -> None:
        Demonstrates an error embed.

    autocomplete_example(interaction: Interaction, choice: str) -> None:
        Demonstrates the autocomplete utility.

    sku_check_example(interaction: Interaction, sku_id: int, user_id: int) -> None:
        Demonstrates the SKU check utility.

    disallow_bots_example(interaction: Interaction, user: discord.User) -> None:
        Demonstrates the disallow bots decorator.

    is_owner_example(interaction: Interaction) -> None:
        Demonstrates the is_owner decorator.
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
        """An example of a main embed."""
        embed = MainEmbed(
            title="Main Embed Example",
            description="This is an example of a main embed.",
        )
        embed.add_field(name="Field 1", value="This is the first field.")
        embed.add_field(name="Field 2", value="This is the second field.")
        await interaction.response.send_message(embed=embed)

    @embed_cmds.command(name="success-embed")
    async def success_embed(self, interaction: Interaction) -> None:
        """An example of a success embed."""
        embed = SuccessEmbed(
            title="Success Embed Example",
            description="This is an example of a success embed.",
        )
        embed.add_field(name="Field 1", value="This is the first field.")
        embed.add_field(name="Field 2", value="This is the second field.")
        await interaction.response.send_message(embed=embed)

    @embed_cmds.command(name="error-embed")
    async def error_embed(self, interaction: Interaction) -> None:
        """An example of an error embed."""
        embed = ErrorEmbed(
            title="Error Embed Example",
            description="This is an example of an error embed.",
        )
        embed.add_field(name="Field 1", value="This is the first field.")
        embed.add_field(name="Field 2", value="This is the second field.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="autocomplete")
    @app_commands.describe(
        choice="The option selected from the autocomplete list."
    )
    @app_commands.autocomplete(
        choice=make_autocomplete("Option 1", "Option 2", "Option 3")
    )
    async def autocomplete_example(
        self, interaction: Interaction, choice: str
    ) -> None:
        """An example of the autocomplete utility."""
        await interaction.response.send_message(f"You selected: {choice}")

    @app_commands.command(name="sku-check")
    @app_commands.describe(
        sku_id="The SKU ID of the package to check.",
        user_id="The Discord user ID to check.",
    )
    async def sku_check_example(
        self, interaction: Interaction, sku_id: int, user_id: int
    ) -> None:
        """An example of the SKU check utility."""
        has_sku = await sku_check(self.bot, sku_id, user_id)
        await interaction.response.send_message(f"User has SKU: {has_sku}")

    @app_commands.command(name="disallow-bots")
    @app_commands.describe(user="The Discord user to check.")
    @disallow_bots
    async def disallow_bots_example(
        self, interaction: Interaction, user: discord.User
    ) -> None:
        """An example of the disallow bots decorator."""
        await interaction.response.send_message(f"User: {user.name}")

    @app_commands.command(name="is-owner")
    @is_owner
    async def is_owner_example(self, interaction: Interaction) -> None:
        """An example of the is_owner decorator."""
        await interaction.response.send_message("You are the owner!")


async def setup(bot: Bot) -> None:
    """
    Asynchronously adds the `Examples` cog to the bot instance.

    Parameters:
    -----------
    bot : Bot
        The bot instance to add the cog to.
    """
    await bot.add_cog(Examples(bot))
