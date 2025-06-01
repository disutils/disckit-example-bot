from typing import Any

import discord
from disckit.utils import SuccessEmbed
from disckit.utils.ui import BaseView


class HomeView(BaseView):
    """
    A view with a single button labeled "Home View".
    """

    def __init__(self, author: discord.User | discord.Member) -> None:
        super().__init__(author=author)

    @discord.ui.button(label="Home View", style=discord.ButtonStyle.primary)
    async def home_button_callback(
        self, interaction: discord.Interaction, _button: discord.ui.Button[Any]
    ) -> None:
        await interaction.response.send_message(
            embed=SuccessEmbed("Home View", "Home View button clicked."),
            ephemeral=True,
        )


def get_extra_buttons() -> list[discord.ui.Button[Any]]:
    """
    Returns a list of buttons labeled from A to S with various styles.
    """
    labels = list("ABCDEFGHIJKLMNOPQRS")
    styles = [
        discord.ButtonStyle.primary,
        discord.ButtonStyle.secondary,
        discord.ButtonStyle.success,
        discord.ButtonStyle.danger,
        discord.ButtonStyle.blurple,  # replaced blurple with primary
    ]

    buttons = []
    for i, label in enumerate(labels):
        style = styles[i % len(styles)]
        buttons.append(discord.ui.Button(label=label, style=style))
    return buttons
