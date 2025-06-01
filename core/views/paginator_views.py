from typing import Any

import discord
from disckit.utils import SuccessEmbed
from disckit.utils.ui import BaseView


class HomeView(BaseView):
    """
    A view representing the home page.

    Parameters
    ----------
    author : discord.User or discord.Member
        The author of the view.
    """

    def __init__(self, author: discord.User | discord.Member) -> None:
        """
        Initialize the HomeView.

        Parameters
        ----------
        author : discord.User or discord.Member
            The author of the view.
        """
        super().__init__(author=author)

    @discord.ui.button(label="Home View", style=discord.ButtonStyle.primary)
    async def home_button_callback(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button[Any],
    ) -> None:
        """
        Callback for the home view button.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction object.
        button : discord.ui.Button[Any]
            The button that was clicked.
        """
        await interaction.response.send_message(
            embed=SuccessEmbed("Home View", "Home View button clicked."),
            ephemeral=True,
        )


def get_extra_buttons() -> list[discord.ui.Button[Any]]:
    """
    Generate a list of extra buttons with various styles.

    Returns
    -------
    list[discord.ui.Button[Any]]
        A list of buttons with different labels and styles.
    """
    labels: list[str] = list("ABCDEFGHIJKLMNOPQRS")
    styles: list[discord.ButtonStyle] = [
        discord.ButtonStyle.primary,
        discord.ButtonStyle.secondary,
        discord.ButtonStyle.success,
        discord.ButtonStyle.danger,
        discord.ButtonStyle.blurple,
    ]

    buttons: list[discord.ui.Button[Any]] = []
    for i, label in enumerate(labels):
        style = styles[i % len(styles)]
        buttons.append(discord.ui.Button(label=label, style=style))
    return buttons
