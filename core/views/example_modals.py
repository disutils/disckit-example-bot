from typing import override

import discord
from disckit.utils.embeds import SuccessEmbed
from disckit.utils.ui import BaseModal


class ModalView(BaseModal):
    """
    A custom modal view extending BaseModal for advanced interaction handling.

    Parameters
    ----------
    title : str, optional
        The title of the modal (default is "Default Modal").
    timeout : float or None, optional
        Timeout in seconds before the modal stops accepting input (default is None).
    custom_id : str, optional
        The custom ID of the modal (default is "modal_view").
    author : int or discord.User or discord.Member or None, optional
        The author restricting usage to a specific user (default is None).
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
        Initialize the ModalView instance.

        Parameters
        ----------
        title : str
            The title of the modal.
        timeout : float or None
            Timeout in seconds before the modal stops accepting input.
        custom_id : str
            The custom ID of the modal.
        author : int or discord.User or discord.Member or None
            The author of the modal.
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
        Handle the submission of the modal.

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
