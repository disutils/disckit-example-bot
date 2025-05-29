"""
This module defines views for the `Examples` cog.

Classes:
--------
- DisableOnClickView: A view that disables all items when the button is clicked.
- DisableOnTimeoutView: A view that disables all items when it times out.
- MultiButtonView: A view with multiple buttons demonstrating different behaviors.

Classes Details:
----------------
- DisableOnClickView:
    Attributes:
    -----------
    - author : discord.User | discord.Member
        The user or member who initiated the view.

    Methods:
    --------
    - disable_button_callback(interaction: discord.Interaction, _button: discord.ui.Button[Any]) -> None:
        Disables all items in the view and sends a success message.

- DisableOnTimeoutView:
    Attributes:
    -----------
    - author : discord.User | discord.Member
        The user or member who initiated the view.
    - timeout : float
        The timeout duration in seconds.

    Methods:
    --------
    - timeout_button_callback(interaction: discord.Interaction, _button: discord.ui.Button[Any]) -> None:
        Sends a success message if clicked before the view times out.

- MultiButtonView:
    Attributes:
    -----------
    - author : discord.User | discord.Member
        The user or member who initiated the view.

    Methods:
    --------
    - disable_all_callback(interaction: discord.Interaction, _button: discord.ui.Button[Any]) -> None:
        Disables all items in the view and sends a success message.
    - do_nothing_callback(interaction: discord.Interaction, _button: discord.ui.Button[Any]) -> None:
        Sends a message indicating no action was taken.
"""

from typing import Any

import discord
from disckit.utils import SuccessEmbed
from disckit.utils.ui import BaseView


class DisableOnClickView(BaseView):
    """
    A view that disables all items when the button is clicked.

    Attributes:
    -----------
    author : discord.User | discord.Member
        The user or member who initiated the view.

    Methods:
    --------
    disable_button_callback(interaction: discord.Interaction, _button: discord.ui.Button[Any]) -> None:
        Disables all items in the view and sends a success message.
    """

    def __init__(self, author: discord.User | discord.Member) -> None:
        """
        Initializes the DisableOnClickView.

        Parameters:
        -----------
        author : discord.User | discord.Member
            The user or member who initiated the view.
        """
        super().__init__(author=author)

    @discord.ui.button(label="Disable Me!", style=discord.ButtonStyle.danger)
    async def disable_button_callback(
        self, interaction: discord.Interaction, _button: discord.ui.Button[Any]
    ) -> None:
        """
        Callback for the "Disable Me!" button.

        Disables all items in the view and sends a success message.

        Parameters:
        -----------
        interaction : discord.Interaction
            The interaction that triggered the button click.
        _button : discord.ui.Button[Any]
            The button that was clicked (unused).
        """
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(
            embed=SuccessEmbed("Disabled!", "All buttons have been disabled."),
            ephemeral=True,
        )


class DisableOnTimeoutView(BaseView):
    """
    A view that disables all items when it times out.

    Attributes:
    -----------
    author : discord.User | discord.Member
        The user or member who initiated the view.
    timeout : float
        The timeout duration in seconds.

    Methods:
    --------
    timeout_button_callback(interaction: discord.Interaction, _button: discord.ui.Button[Any]) -> None:
        Sends a success message if clicked before the view times out.
    """

    def __init__(
        self, author: discord.User | discord.Member, timeout: float = 10.0
    ) -> None:
        """
        Initializes the DisableOnTimeoutView.

        Parameters:
        -----------
        author : discord.User | discord.Member
            The user or member who initiated the view.
        timeout : float, optional
            The timeout duration in seconds (default is 10.0).
        """
        super().__init__(author=author, timeout=timeout)

    @discord.ui.button(
        label="Click Me Before Timeout!", style=discord.ButtonStyle.primary
    )
    async def timeout_button_callback(
        self, interaction: discord.Interaction, _button: discord.ui.Button[Any]
    ) -> None:
        """
        Callback for the "Click Me Before Timeout!" button.

        Sends a success message if clicked before the view times out.

        Parameters:
        -----------
        interaction : discord.Interaction
            The interaction that triggered the button click.
        _button : discord.ui.Button[Any]
            The button that was clicked (unused).
        """
        await interaction.response.send_message(
            embed=SuccessEmbed("Clicked!", "You clicked before timeout."),
            ephemeral=True,
        )


class MultiButtonView(BaseView):
    """
    A view with multiple buttons demonstrating different behaviors.

    Attributes:
    -----------
    author : discord.User | discord.Member
        The user or member who initiated the view.

    Methods:
    --------
    disable_all_callback(interaction: discord.Interaction, _button: discord.ui.Button[Any]) -> None:
        Disables all items in the view and sends a success message.

    do_nothing_callback(interaction: discord.Interaction, _button: discord.ui.Button[Any]) -> None:
        Sends a message indicating no action was taken.
    """

    def __init__(self, author: discord.User | discord.Member) -> None:
        """
        Initializes the MultiButtonView.

        Parameters:
        -----------
        author : discord.User | discord.Member
            The user or member who initiated the view.
        """
        super().__init__(author=author)

    @discord.ui.button(label="Disable All", style=discord.ButtonStyle.danger)
    async def disable_all_callback(
        self, interaction: discord.Interaction, _button: discord.ui.Button[Any]
    ) -> None:
        """
        Callback for the "Disable All" button.

        Disables all items in the view and sends a success message.

        Parameters:
        -----------
        interaction : discord.Interaction
            The interaction that triggered the button click.
        _button : discord.ui.Button[Any]
            The button that was clicked (unused).
        """
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(
            embed=SuccessEmbed("Disabled!", "All buttons have been disabled."),
            ephemeral=True,
        )

    @discord.ui.button(label="Do Nothing", style=discord.ButtonStyle.secondary)
    async def do_nothing_callback(
        self, interaction: discord.Interaction, _button: discord.ui.Button[Any]
    ) -> None:
        """
        Callback for the "Do Nothing" button.

        Sends a message indicating no action was taken.

        Parameters:
        -----------
        interaction : discord.Interaction
            The interaction that triggered the button click.
        _button : discord.ui.Button[Any]
            The button that was clicked (unused).
        """
        await interaction.response.send_message(
            embed=SuccessEmbed("No Action", "This button does nothing."),
            ephemeral=True,
        )
