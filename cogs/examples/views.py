"""
This module defines commands related to views for the `ViewCommands` cog.

Classes:
--------
- ViewCommands: A cog containing commands related to views.

Functions:
----------
- setup(bot: Bot) -> None:
    Asynchronously adds the `ViewCommands` cog to the bot instance.

Commands:
---------
- view disable-on-click: Demonstrates a view that disables all buttons on click.
- view disable-on-timeout: Demonstrates a view that disables all buttons on timeout.
- view multi-button: Demonstrates a view with multiple buttons and behaviors.
- view modal-example: Demonstrates a modal interaction.
- view paginator-example: Demonstrates a paginator interaction.
"""

import logging

from disckit.cogs import BaseCog
from disckit.utils.embeds import MainEmbed
from disckit.utils.paginator import Paginator
from discord import Interaction, app_commands

from core import Bot
from core.views.example_modals import ModalView
from core.views.example_views import (
    DisableOnClickView,
    DisableOnTimeoutView,
    MultiButtonView,
)
from core.views.paginator_views import HomeView, get_extra_buttons

logger = logging.getLogger(__name__)


class ViewCommands(BaseCog, name="View Commands"):
    """
    A cog containing commands related to views.

    Attributes:
    -----------
    view_cmds : app_commands.Group
        A command group for view-related commands.

    Methods:
    --------
    disable_on_click(interaction: Interaction) -> None:
        Demonstrates a view that disables all buttons on click.

    disable_on_timeout(interaction: Interaction) -> None:
        Demonstrates a view that disables all buttons on timeout.

    multi_button(interaction: Interaction) -> None:
        Demonstrates a view with multiple buttons and behaviors.

    modal_example(interaction: Interaction) -> None:
        Demonstrates a modal interaction.
    """

    def __init__(self, bot: Bot) -> None:
        super().__init__(logger=logger)
        self.bot: Bot = bot

    view_cmds: app_commands.Group = app_commands.Group(
        name="view",
        description="Commands related to views.",
        guild_only=True,
    )

    @view_cmds.command(name="disable-on-click")
    async def disable_on_click(self, interaction: Interaction) -> None:
        """
        An example of a view that disables all buttons on click.

        Parameters
        ----------
        interaction : Interaction
            The interaction that triggered this command.
        """
        view = DisableOnClickView(author=interaction.user)
        await interaction.response.send_message(
            "Here is a view that disables on click:", view=view
        )
        view.message = (
            await interaction.original_response()
        )  # Required for the view to work properly

    @view_cmds.command(name="disable-on-timeout")
    async def disable_on_timeout(self, interaction: Interaction) -> None:
        """
        An example of a view that disables all buttons on timeout.

        Parameters
        ----------
        interaction : Interaction
            The interaction that triggered this command.
        """
        view = DisableOnTimeoutView(author=interaction.user, timeout=10.0)
        await interaction.response.send_message(
            "Here is a view that disables on timeout:", view=view
        )
        view.message = (
            await interaction.original_response()
        )  # Required for the view to work properly

    @view_cmds.command(name="multi-button")
    async def multi_button(self, interaction: Interaction) -> None:
        """
        An example of a view with multiple buttons and behaviors.

        Parameters
        ----------
        interaction : Interaction
            The interaction that triggered this command.
        """
        view = MultiButtonView(author=interaction.user)
        await interaction.response.send_message(
            "Here is a view with multiple buttons:", view=view
        )
        view.message = (
            await interaction.original_response()
        )  # Required for the view to work properly

    @view_cmds.command(name="modal-example")
    async def modal_example(self, interaction: Interaction) -> None:
        """
        An example of a modal interaction.

        Parameters
        ----------
        interaction : Interaction
            The interaction that triggered this command.
        """
        modal = ModalView(
            title="Example Modal",
            author=interaction.user,
        )
        await interaction.response.send_modal(modal)

    @view_cmds.command(name="paginator-example")
    async def paginator_example(self, interaction: Interaction) -> None:
        """
        An example of a paginator interaction.

        Parameters
        ----------
        interaction : Interaction
            The interaction that triggered this command.
        """
        pages: list[MainEmbed | str] = [
            "Page 1: Welcome to the paginator!",
            "Page 2: This is the second page.",
            "Page 3: You can add as many pages as you want.",
            MainEmbed("Page 4", "This is an embed page."),
        ]

        paginator = Paginator(
            interaction=interaction,
            pages=list(pages),
            author=interaction.user.id,
            home_page="Home Page: This is the starting page.",
            home_view=HomeView(author=interaction.user),
            extra_buttons=get_extra_buttons(),
        )

        await paginator.start()


async def setup(bot: Bot) -> None:
    """
    Asynchronously adds the `ViewCommands` cog to the bot instance.

    Parameters
    ----------
    bot : Bot
        The bot instance to add the cog to.
    """
    await bot.add_cog(ViewCommands(bot))
