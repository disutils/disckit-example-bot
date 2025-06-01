import discord
from disckit.utils import SuccessEmbed
from disckit.utils.ui import BaseView

from typing import Any

class DisableOnClickView(BaseView):
    """
    A view that disables all buttons when one is clicked.

    Parameters
    ----------
    author : discord.User or discord.Member
        The author of the view.
    """

    def __init__(self, author: discord.User | discord.Member) -> None:
        """
        Initialize the DisableOnClickView.

        Parameters
        ----------
        author : discord.User or discord.Member
            The author of the view.
        """
        super().__init__(author=author)

    @discord.ui.button(label="Disable Me!", style=discord.ButtonStyle.danger)
    async def disable_button_callback(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[Any],
    ) -> None:
        """
        Callback to disable all buttons when clicked.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction object.
        button : discord.ui.Button[Any]
            The button that was clicked.
        """
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(
            embed=SuccessEmbed("Disabled!", "All buttons have been disabled."),
            ephemeral=True,
        )


class DisableOnTimeoutView(BaseView):
    """
    A view that disables all buttons after a timeout.

    Parameters
    ----------
    author : discord.User or discord.Member
        The author of the view.
    timeout : float, optional
        The timeout duration in seconds, by default 10.0.
    """

    def __init__(
        self, author: discord.User | discord.Member, timeout: float = 10.0
    ) -> None:
        """
        Initialize the DisableOnTimeoutView.

        Parameters
        ----------
        author : discord.User or discord.Member
            The author of the view.
        timeout : float, optional
            The timeout duration in seconds, by default 10.0.
        """
        super().__init__(author=author, timeout=timeout)

    @discord.ui.button(
        label="Click Me Before Timeout!", style=discord.ButtonStyle.primary
    )
    async def timeout_button_callback(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[Any],
    ) -> None:
        """
        Callback to handle button clicks before timeout.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction object.
        button : discord.ui.Button[Any]
            The button that was clicked.
        """
        await interaction.response.send_message(
            embed=SuccessEmbed("Clicked!", "You clicked before timeout."),
            ephemeral=True,
        )


class MultiButtonView(BaseView):
    """
    A view with multiple buttons for various actions.

    Parameters
    ----------
    author : discord.User or discord.Member
        The author of the view.
    """

    def __init__(self, author: discord.User | discord.Member) -> None:
        """
        Initialize the MultiButtonView.

        Parameters
        ----------
        author : discord.User or discord.Member
            The author of the view.
        """
        super().__init__(author=author)

    @discord.ui.button(label="Disable All", style=discord.ButtonStyle.danger)
    async def disable_all_callback(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[Any],
    ) -> None:
        """
        Callback to disable all buttons when clicked.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction object.
        button : discord.ui.Button[Any]
            The button that was clicked.
        """
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(
            embed=SuccessEmbed("Disabled!", "All buttons have been disabled."),
            ephemeral=True,
        )

    @discord.ui.button(label="Do Nothing", style=discord.ButtonStyle.secondary)
    async def do_nothing_callback(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[Any],
    ) -> None:
        """
        Callback for a button that performs no action.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction object.
        button : discord.ui.Button[Any]
            The button that was clicked.
        """
        await interaction.response.send_message(
            embed=SuccessEmbed("No Action", "This button does nothing."),
            ephemeral=True,
        )
