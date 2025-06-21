from discord import User, Member, Interaction, ButtonStyle
from disckit.utils import SuccessEmbed
from disckit.utils.ui import BaseView
from discord.ui import View, Button, button


class HomeView(BaseView):
    """
    A view representing the home page.

    Parameters
    ----------
    author : User or Member
        The author of the view.
    """

    def __init__(self, author: User | Member) -> None:
        """
        Initialize the HomeView.

        Parameters
        ----------
        author : User or Member
            The author of the view.
        """
        super().__init__(author=author)

    @button(label="Home View", style=ButtonStyle.primary)
    async def home_button_callback(
        self,
        interaction: Interaction,
        button: Button[View],
    ) -> None:
        """
        Callback for the home view button.

        Parameters
        ----------
        interaction : Interaction
            The interaction object.
        button : Button[View]
            The button that was clicked.
        """
        await interaction.response.send_message(
            embed=SuccessEmbed("Home View", "Home View button clicked."),
            ephemeral=True,
        )


def get_extra_buttons() -> list[Button[View]]:
    """
    Generate a list of extra buttons with various styles.

    Returns
    -------
    list[Button[View]]
        A list of buttons with different labels and styles.
    """
    labels: list[str] = list("ABCDEFGHIJKLMOP")
    styles: list[ButtonStyle] = [
        ButtonStyle.primary,
        ButtonStyle.secondary,
        ButtonStyle.success,
        ButtonStyle.danger,
        ButtonStyle.blurple,
    ]

    buttons: list[Button[View]] = []
    for i, label in enumerate(labels):
        style = styles[i % len(styles)]
        buttons.append(Button(label=label, style=style))
    return buttons
