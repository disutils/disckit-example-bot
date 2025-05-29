"""
This module defines the `Examples` cog for the Discord bot, showcasing various utilities provided by `disckit.utils`.

Classes:
--------
- Examples: A cog containing example commands for utilities like embeds, autocomplete, decorators, and views.

Functions:
----------
- setup(bot: Bot) -> None:
    Asynchronously adds the `Examples` cog to the bot instance.
"""

import logging
from typing import override

import discord
from disckit.utils import disallow_bots, is_owner, make_autocomplete, sku_check
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
