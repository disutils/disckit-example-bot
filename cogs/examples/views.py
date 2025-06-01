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

logger: logging.Logger = logging.getLogger(__name__)


class ViewCommands(BaseCog, name="View Commands"):
    """
    A cog for demonstrating view-related commands.

    Parameters
    ----------
    bot : Bot
        The bot instance.
    """

    def __init__(self, bot: Bot) -> None:
        """
        Initialize the ViewCommands cog.

        Parameters
        ----------
        bot : Bot
            The bot instance.
        """
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
        Send a view that disables on click.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        """
        view = DisableOnClickView(author=interaction.user)
        await interaction.response.send_message(
            "Here is a view that disables on click:", view=view
        )
        view.message = (
            await interaction.original_response()
        )  # Required to store the message for later updates

    @view_cmds.command(name="disable-on-timeout")
    async def disable_on_timeout(self, interaction: Interaction) -> None:
        """
        Send a view that disables on timeout.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        """
        view = DisableOnTimeoutView(author=interaction.user, timeout=10.0)
        await interaction.response.send_message(
            "Here is a view that disables on timeout:", view=view
        )
        view.message = (
            await interaction.original_response()
        )  # Required to store the message for later updates

    @view_cmds.command(name="multi-button")
    async def multi_button(self, interaction: Interaction) -> None:
        """
        Send a view with multiple buttons.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        """
        view = MultiButtonView(author=interaction.user)
        await interaction.response.send_message(
            "Here is a view with multiple buttons:", view=view
        )
        view.message = (
            await interaction.original_response()
        )  # Required to store the message for later updates

    @view_cmds.command(name="modal-example")
    async def modal_example(self, interaction: Interaction) -> None:
        """
        Send an example modal.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        """
        modal = ModalView(
            title="Example Modal",
            author=interaction.user,
        )
        await interaction.response.send_modal(modal)

    @view_cmds.command(name="paginator-example")
    async def paginator_example(self, interaction: Interaction) -> None:
        """
        Send an example paginator.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
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
    Set up the ViewCommands cog.

    Parameters
    ----------
    bot : Bot
        The bot instance.
    """
    await bot.add_cog(ViewCommands(bot))
