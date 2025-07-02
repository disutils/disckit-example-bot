import logging

from disckit.cogs import BaseCog
from disckit.utils import (
    disallow_bots,
    is_owner,
    make_autocomplete,
    sku_check_guild,
    sku_check_user,
)
from discord import Interaction, User, app_commands

from core import Bot

_logger: logging.Logger = logging.getLogger(__name__)


class Examples(BaseCog, name="Examples"):
    """
    A cog for demonstrating various example commands.

    Parameters
    ----------
    bot : Bot
        The bot instance.
    """

    def __init__(self, bot: Bot) -> None:
        """
        Initialize the Examples cog.

        Parameters
        ----------
        bot : Bot
            The bot instance.
        """
        super().__init__(logger=_logger)
        self.bot: Bot = bot

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
        """
        Demonstrate an autocomplete command.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        choice : str
            The selected option from the autocomplete list.
        """
        await interaction.response.send_message(f"You selected: {choice}")

    @app_commands.command(name="sku-check-user")
    @app_commands.describe(
        sku_id="The SKU ID of the package to check.",
        user_id="The Discord user ID to check.",
    )
    async def sku_check_user_example(
        self, interaction: Interaction, sku_id: int, user_id: int
    ) -> None:
        """
        Check if a user has a specific SKU.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        sku_id : int
            The SKU ID of the package to check.
        user_id : int
            The Discord user ID to check.
        """
        has_sku = await sku_check_user(
            bot=self.bot, sku_id=sku_id, user_id=user_id
        )
        await interaction.response.send_message(f"User has SKU: {has_sku}")

    @app_commands.command(name="sku-check-guild")
    @app_commands.describe(
        sku_id="The SKU ID of the package to check.",
        guild_id="The Discord user ID to check.",
    )
    async def sku_check_guild_example(
        self, interaction: Interaction, sku_id: int, guild_id: int
    ) -> None:
        """
        Check if a user has a specific SKU.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        sku_id : int
            The SKU ID of the package to check.
        guild_id : int
            The Discord guild ID to check.
        """
        has_sku = await sku_check_guild(
            bot=self.bot, sku_id=sku_id, guild_id=guild_id
        )
        await interaction.response.send_message(f"Guild has SKU: {has_sku}")

    @app_commands.command(name="disallow-bots")
    @app_commands.describe(user="The Discord user to check.")
    @disallow_bots()
    async def disallow_bots_example(
        self, interaction: Interaction, user: User
    ) -> None:
        """
        Demonstrate a command that disallows bots.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        user : User
            The Discord user to check.
        """
        await interaction.response.send_message(f"User: {user.name}")

    @app_commands.command(name="is-owner")
    @is_owner()
    async def is_owner_example(self, interaction: Interaction) -> None:
        """
        Demonstrate a command restricted to the bot owner.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        """
        await interaction.response.send_message("You are the owner!")


async def setup(bot: Bot) -> None:
    """
    Set up the Examples cog.

    Parameters
    ----------
    bot : Bot
        The bot instance.
    """
    await bot.add_cog(Examples(bot))
