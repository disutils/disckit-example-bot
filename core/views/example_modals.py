from typing import override

import discord
from disckit.utils.embeds import SuccessEmbed
from disckit.utils.ui import BaseModal
from discord.ui import View


class ModalView(BaseModal):
    """
    A modal view for collecting user input.

    Parameters
    ----------
    title : str, optional
        The title of the modal, by default "Default Modal".
    timeout : float or None, optional
        The timeout duration for the modal, by default None.
    custom_id : str, optional
        The custom ID for the modal, by default "modal_view".
    author : int or discord.User or discord.Member or None, optional
        The author of the modal, by default None.
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
        Initialize the ModalView.

        Parameters
        ----------
        title : str, optional
            The title of the modal, by default "Default Modal".
        timeout : float or None, optional
            The timeout duration for the modal, by default None.
        custom_id : str, optional
            The custom ID for the modal, by default "modal_view".
        author : int or discord.User or discord.Member or None, optional
            The author of the modal, by default None.
        """
        super().__init__(
            title=title, timeout=timeout, custom_id=custom_id, author=author
        )

        self.input_field: discord.ui.TextInput[View] = discord.ui.TextInput(
            label="Your Input",
            placeholder="Enter something here...",
            max_length=100,
        )
        self.add_item(self.input_field)

    @override
    async def on_submit(self, interaction: discord.Interaction) -> None:
        """
        Handle the submission of the modal.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction object representing the modal submission.
        """
        user_input: str = self.input_field.value
        await interaction.response.send_message(
            embed=SuccessEmbed(
                "Modal Submitted",
                f"Your input: {user_input}",
            ),
            ephemeral=True,
        )
