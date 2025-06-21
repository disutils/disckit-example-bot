from discord import User, Member, Interaction, ButtonStyle
from disckit.utils import SuccessEmbed
from disckit.utils.ui import BaseView
from discord.ui import View, Button, button


class DisableOnClickView(BaseView):
    """
    A view that disables all buttons when one is clicked.

    Parameters
    ----------
    author : User or Member
        The author of the view.
    """

    def __init__(self, author: User | Member) -> None:
        """
        Initialize the DisableOnClickView.

        Parameters
        ----------
        author : User or Member
            The author of the view.
        """
        super().__init__(author=author)

    button(label="Disable Me!", style=ButtonStyle.danger)
    async def disable_button_callback(
        self,
        interaction: Interaction,
        button: Button[View],
    ) -> None:
        """
        Callback to disable all buttons when clicked.

        Parameters
        ----------
        interaction : Interaction
            The interaction object.
        button : Button[View]
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
    author : User or Member
        The author of the view.
    timeout : float, optional
        The timeout duration in seconds, by default 10.0.
    """

    def __init__(
        self, author: User | Member, timeout: float = 10.0
    ) -> None:
        """
        Initialize the DisableOnTimeoutView.

        Parameters
        ----------
        author : User or Member
            The author of the view.
        timeout : float, optional
            The timeout duration in seconds, by default 10.0.
        """
        super().__init__(author=author, timeout=timeout)

    button(
        label="Click Me Before Timeout!", style=ButtonStyle.primary
    )
    async def timeout_button_callback(
        self,
        interaction: Interaction,
        button: Button[View],
    ) -> None:
        """
        Callback to handle button clicks before timeout.

        Parameters
        ----------
        interaction : Interaction
            The interaction object.
        button : Button[View]
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
    author : User or Member
        The author of the view.
    """

    def __init__(self, author: User | Member) -> None:
        """
        Initialize the MultiButtonView.

        Parameters
        ----------
        author : User or Member
            The author of the view.
        """
        super().__init__(author=author)

    button(label="Disable All", style=ButtonStyle.danger)
    async def disable_all_callback(
        self,
        interaction: Interaction,
        button: Button[View],
    ) -> None:
        """
        Callback to disable all buttons when clicked.

        Parameters
        ----------
        interaction : Interaction
            The interaction object.
        button : Button[View]
            The button that was clicked.
        """
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(
            embed=SuccessEmbed("Disabled!", "All buttons have been disabled."),
            ephemeral=True,
        )

    button(label="Do Nothing", style=ButtonStyle.secondary)
    async def do_nothing_callback(
        self,
        interaction: Interaction,
        button: Button[View],
    ) -> None:
        """
        Callback for a button that performs no action.

        Parameters
        ----------
        interaction : Interaction
            The interaction object.
        button : Button[View]
            The button that was clicked.
        """
        await interaction.response.send_message(
            embed=SuccessEmbed("No Action", "This button does nothing."),
            ephemeral=True,
        )
