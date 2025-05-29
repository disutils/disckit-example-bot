"""
This module defines the `HomeView` class and `ExtraButtons` for the `Home` cog.

Classes:
--------
- HomeView: A view with a single button that sends a response when clicked.

Functions:
----------
- get_extra_buttons() -> list[discord.ui.Button[Any]]:
    Returns a list of buttons for use in messages.
"""

from typing import Any

import discord
from disckit.utils import SuccessEmbed
from disckit.utils.ui import BaseView


class HomeView(BaseView):
    """
    A view with a single button labeled "Home View".

    Attributes:
    -----------
    author : discord.User | discord.Member
        The user or member who initiated the view.

    Methods:
    --------
    home_button_callback(interaction: discord.Interaction, _button: discord.ui.Button[Any]) -> None:
        Sends a response indicating the button was clicked.
    """

    def __init__(self, author: discord.User | discord.Member) -> None:
        """
        Initializes the HomeView.

        Parameters:
        -----------
        author : discord.User | discord.Member
            The user or member who initiated the view.
        """
        super().__init__(author=author)

    @discord.ui.button(label="Home View", style=discord.ButtonStyle.primary)
    async def home_button_callback(
        self, interaction: discord.Interaction, _button: discord.ui.Button[Any]
    ) -> None:
        """
        Callback for the "Home View" button.

        Sends a response indicating the button was clicked.

        Parameters:
        -----------
        interaction : discord.Interaction
            The interaction that triggered the button click.
        _button : discord.ui.Button[Any]
            The button that was clicked (unused).
        """
        await interaction.response.send_message(
            embed=SuccessEmbed("Home View", "Home View button clicked."),
            ephemeral=True,
        )


def get_extra_buttons() -> list[discord.ui.Button[Any]]:
    """
    Returns a list of buttons labeled from A to T for use in messages.

    Returns:
    --------
    list[discord.ui.Button[Any]]:
        A list of buttons.
    """
    return [
        discord.ui.Button(label="A", style=discord.ButtonStyle.primary),
        discord.ui.Button(label="B", style=discord.ButtonStyle.secondary),
        discord.ui.Button(label="C", style=discord.ButtonStyle.success),
        discord.ui.Button(label="D", style=discord.ButtonStyle.danger),
        discord.ui.Button(label="E", style=discord.ButtonStyle.blurple),
        discord.ui.Button(label="F", style=discord.ButtonStyle.primary),
        discord.ui.Button(label="G", style=discord.ButtonStyle.secondary),
        discord.ui.Button(label="H", style=discord.ButtonStyle.success),
        discord.ui.Button(label="I", style=discord.ButtonStyle.danger),
        discord.ui.Button(label="J", style=discord.ButtonStyle.blurple),
        discord.ui.Button(label="K", style=discord.ButtonStyle.primary),
        discord.ui.Button(label="L", style=discord.ButtonStyle.secondary),
        discord.ui.Button(label="M", style=discord.ButtonStyle.success),
        discord.ui.Button(label="N", style=discord.ButtonStyle.danger),
        discord.ui.Button(label="O", style=discord.ButtonStyle.blurple),
        discord.ui.Button(label="P", style=discord.ButtonStyle.primary),
        discord.ui.Button(label="Q", style=discord.ButtonStyle.secondary),
        discord.ui.Button(label="R", style=discord.ButtonStyle.success),
        discord.ui.Button(label="S", style=discord.ButtonStyle.danger),
    ]
