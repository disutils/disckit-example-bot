from typing import override

import discord
from disckit import UtilConfig
from disckit.utils.mention_tree import MentionTree
from discord.ext import commands

from core.config import OWNER_IDS, BotData
from core.updater import check_bot_updates


class Bot(commands.AutoShardedBot):
    """
    Represents the main bot instance.

    This class extends `commands.AutoShardedBot` and provides custom behavior for the bot's setup process,
    including command synchronization and dynamic configuration updates.

    Attributes
    ----------
    tree : MentionTree
        The custom command tree used for handling interactions.
    """

    def __init__(self, intents: discord.Intents) -> None:
        """
        Initialize the bot instance.

        Parameters
        ----------
        intents : discord.Intents
            The intents to be used by the bot for interacting with Discord.
        """
        super().__init__(
            command_prefix="/",
            intents=intents,
            help_command=None,
            tree_cls=MentionTree,
            owner_ids=OWNER_IDS,
            chunk_guilds_at_startup=False,
        )
        self.tree: MentionTree

    @override
    async def setup_hook(self) -> None:
        """
        Called when the bot logs in.

        This method handles the synchronization of commands and updates bot-related configurations,
        such as the avatar URL and footer image.
        """
        # from core.config import SYNC_GUILD_ID
        #
        # synced_global = await self.tree.sync()
        # synced_guild = await self.tree.sync(
        #     guild=discord.Object(SYNC_GUILD_ID)
        # )
        #
        # global_cmds = len(synced_global)
        # guild_cmds = len(synced_guild)
        # print(f"Synced {global_cmds} global commands.")
        # print(f"Synced {guild_cmds} guild commands.")

        if self.user is not None:
            if self.user.avatar:
                BotData.AVATAR_URL = self.user.avatar.url
            else:
                BotData.AVATAR_URL = None

            UtilConfig.FOOTER_IMAGE = BotData.AVATAR_URL
            print(
                f"\033[93m{self.user.name} has logged in successfully.\033[0m"
            )

            # Check for updates after successful login
            await check_bot_updates()
