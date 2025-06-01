import logging

from disckit.cogs import BaseCog
from disckit.utils.cooldown import CoolDown, CoolDownBucket
from disckit.utils.embeds import ErrorEmbed, SuccessEmbed
from discord import Interaction, app_commands

from core import Bot

logger: logging.Logger = logging.getLogger(__name__)


class CooldownCommands(BaseCog, name="Cooldown Commands"):
    """
    A cog for demonstrating cooldown functionality in commands.

    Parameters
    ----------
    bot : Bot
        The bot instance.
    """

    def __init__(self, bot: Bot) -> None:
        """
        Initialize the CooldownCommands cog.

        Parameters
        ----------
        bot : Bot
            The bot instance.
        """
        super().__init__(logger=logger)
        self.bot: Bot = bot

    cooldown_cmds: app_commands.Group = app_commands.Group(
        name="cooldown",
        description="Commands to demonstrate cooldown functionality.",
        guild_only=True,
    )

    @cooldown_cmds.command(name="user")
    @CoolDown.cooldown(time=10, bucket_type=CoolDownBucket.USER)
    async def user_cooldown(self, interaction: Interaction) -> None:
        """
        Command with a 10-second cooldown per user.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        """
        await interaction.response.send_message(
            embed=SuccessEmbed(
                "User Cooldown",
                "This command is on a 10-second cooldown per user.",
            ),
            ephemeral=True,
        )

    @cooldown_cmds.command(name="guild")
    @CoolDown.cooldown(time=20, bucket_type=CoolDownBucket.GUILD)
    async def guild_cooldown(self, interaction: Interaction) -> None:
        """
        Command with a 20-second cooldown per guild.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        """
        await interaction.response.send_message(
            embed=SuccessEmbed(
                "Guild Cooldown",
                "This command is on a 20-second cooldown per guild.",
            ),
            ephemeral=True,
        )

    @cooldown_cmds.command(name="channel")
    @CoolDown.cooldown(time=15, bucket_type=CoolDownBucket.CHANNEL)
    async def channel_cooldown(self, interaction: Interaction) -> None:
        """
        Command with a 15-second cooldown per channel.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        """
        await interaction.response.send_message(
            embed=SuccessEmbed(
                "Channel Cooldown",
                "This command is on a 15-second cooldown per channel.",
            ),
            ephemeral=True,
        )

    @cooldown_cmds.command(name="sku")
    @CoolDown.cooldown(time=30, bucket_type=CoolDownBucket.USER, sku_id=12345)
    async def sku_cooldown(self, interaction: Interaction) -> None:
        """
        Command with a 30-second cooldown per user, bypassable with SKU.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        """
        await interaction.response.send_message(
            embed=SuccessEmbed(
                "SKU Cooldown",
                "This command is on a 30-second cooldown per user, bypassable with SKU.",
            ),
            ephemeral=True,
        )

    @cooldown_cmds.command(name="dynamic-cooldown")
    async def dynamic_cooldown(self, interaction: Interaction) -> None:
        """
        Command demonstrating dynamic cooldowns.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        """
        if interaction.user.id == 1022085572719808542:
            allowed, cooldown_text = CoolDown.check(
                interaction, CoolDownBucket.USER
            )

            if not allowed:
                await interaction.response.send_message(
                    f"You can use the command in {cooldown_text}"
                )
                return

            CoolDown.add(25, interaction, CoolDownBucket.USER)

        await interaction.response.send_message("Testing dynamic cooldowns")

    @cooldown_cmds.command(name="reset")
    async def reset_cooldown(self, interaction: Interaction) -> None:
        """
        Command to reset the cooldown for the `user` command.

        Parameters
        ----------
        interaction : Interaction
            The Discord interaction.
        """
        reset = CoolDown.reset(
            interaction, bucket_type=CoolDownBucket.USER, command_name="user"
        )
        if reset:
            await interaction.response.send_message(
                embed=SuccessEmbed(
                    "Cooldown Reset", "The cooldown for `user` has been reset."
                ),
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                embed=ErrorEmbed(
                    "Cooldown Reset Failed",
                    "No active cooldown found to reset.",
                ),
                ephemeral=True,
            )


async def setup(bot: Bot) -> None:
    """
    Set up the CooldownCommands cog.

    Parameters
    ----------
    bot : Bot
        The bot instance.
    """
    await bot.add_cog(CooldownCommands(bot))
