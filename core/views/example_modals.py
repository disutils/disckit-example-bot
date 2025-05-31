"""
This module defines a custom `ModalView` class for enhanced modal interactions.

Classes:
--------
- ModalView: A custom modal view that extends `BaseModal` to provide advanced interaction handling.

Attributes:
-----------
- title : str
    The title of the modal (up to 45 characters).
- timeout : float | None
    Timeout in seconds before the modal stops accepting input.
- custom_id : str
    The custom ID of the modal (up to 100 characters).
- author : int | discord.User | discord.Member | None
    The author of the modal, restricting usage to the specified user.

Methods:
--------
- interaction_check(interaction: discord.Interaction) -> bool:
    Ensures the interaction is from the authorized user.
- on_error(interaction: discord.Interaction, error: Exception) -> None:
    Handles errors that occur during modal interactions.
- on_submit(interaction: discord.Interaction) -> None:
    Handles the submission of the modal.
"""

from typing import override

import discord
from disckit.utils.embeds import SuccessEmbed
from disckit.utils.ui import BaseModal


class ModalView(BaseModal):
    """
    A custom modal view that extends `BaseModal` to provide advanced interaction handling.

    Attributes:
    -----------
    title : str
        The title of the modal (up to 45 characters).
    timeout : float | None
        Timeout in seconds before the modal stops accepting input.
    custom_id : str
        The custom ID of the modal (up to 100 characters).
    author : int | discord.User | discord.Member | None
        The author of the modal, restricting usage to the specified user.

    Methods:
    --------
    interaction_check(interaction: discord.Interaction) -> bool:
        Ensures the interaction is from the authorized user.

    on_error(interaction: discord.Interaction, error: Exception) -> None:
        Handles errors that occur during modal interactions.
    """

    def __init__(
        self,
        *,
        title: str = "Default Modal",
        timeout: float | None = None,
        custom_id: str = "modal_view",
        author: int | discord.User | discord.Member | None = None,
    ) -> None:
        """
        Initializes the ModalView.

        Parameters
        ----------
        title : str
            The title of the modal.
        timeout : float | None
            Timeout in seconds before the modal stops accepting input.
        custom_id : str
            The custom ID of the modal.
        author : int | discord.User | discord.Member | None
            The author of the modal, restricting usage to the specified user.
        """
        super().__init__(
            title=title, timeout=timeout, custom_id=custom_id, author=author
        )

        self.input_field: discord.ui.TextInput[BaseModal] = (
            discord.ui.TextInput(
                label="Your Input",
                placeholder="Enter something here...",
                max_length=100,
            )
        )
        self.add_item(self.input_field)

    @override
    async def on_submit(self, interaction: discord.Interaction) -> None:
        """
        Handles the submission of the modal.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction that triggered the modal submission.
        """
        user_input: str = self.input_field.value
        await interaction.response.send_message(
            embed=SuccessEmbed(
                "Modal Submitted",
                f"Your input: {user_input}",
            ),
            ephemeral=True,
        )
