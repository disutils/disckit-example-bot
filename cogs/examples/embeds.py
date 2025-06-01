import logging

from disckit.cogs import BaseCog
from disckit.utils.embeds import ErrorEmbed, MainEmbed, SuccessEmbed
from discord import Interaction, app_commands

from core import Bot

logger: logging.Logger = logging.getLogger(__name__)


class EmbedCommands(BaseCog, name="Embed Commands"):
    """
    A cog for demonstrating embed-related commands.

    Parameters
    ----------
    bot : Bot
        The bot instance.
    """

    def __init__(self, bot: Bot) -> None:
        """
        Initialize the EmbedCommands cog.

        Parameters
        ----------
        bot : Bot
            The bot instance.
        """
        super().__init__(logger=logger)
        self.bot: Bot = bot

    embed_cmds: app_commands.Group = app_commands.Group(
        name="embed",
        description="Commands related to embeds.",
        guild_only=True,
    )

    @embed_cmds.command(name="main-embed")
    async def main_embed(self, interaction: Interaction) -> None:
        """
        Send an example of a main embed.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        """
        embed = MainEmbed(
            "Main Embed Example",
            "This is an example of a main embed.",
        )
        embed.add_field(name="Field 1", value="This is the first field.")
        embed.add_field(name="Field 2", value="This is the second field.")
        await interaction.response.send_message(embed=embed)

    @embed_cmds.command(name="success-embed")
    async def success_embed(self, interaction: Interaction) -> None:
        """
        Send an example of a success embed.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        """
        embed = SuccessEmbed(
            "Success Embed Example",
            "This is an example of a success embed.",
        )
        embed.add_field(name="Field 1", value="This is the first field.")
        embed.add_field(name="Field 2", value="This is the second field.")
        await interaction.response.send_message(embed=embed)

    @embed_cmds.command(name="error-embed")
    async def error_embed(self, interaction: Interaction) -> None:
        """
        Send an example of an error embed.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        """
        embed = ErrorEmbed(
            "Error Embed Example",
            "This is an example of an error embed.",
        )
        embed.add_field(name="Field 1", value="This is the first field.")
        embed.add_field(name="Field 2", value="This is the second field.")
        await interaction.response.send_message(embed=embed)


async def setup(bot: Bot) -> None:
    """
    Set up the EmbedCommands cog.

    Parameters
    ----------
    bot : Bot
        The bot instance.
    """
    await bot.add_cog(EmbedCommands(bot))
