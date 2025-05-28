"""
This module defines the core `Bot` class for the Discord bot, which extends the `commands.AutoShardedBot` class.
It includes custom behavior for command synchronization and bot setup.

Classes:
---------
- Bot: Represents the main bot instance with custom setup logic and configurations.
"""

import discord
from disckit import UtilConfig
from discord.ext import commands

from core.config import OWNER_IDS, BotData
from core.mention_tree import MentionTree


class Bot(commands.AutoShardedBot):
    """
    Represents the main bot instance.

    This class extends `commands.AutoShardedBot` and provides custom behavior for the bot's setup process,
    including command synchronization and dynamic configuration updates.

    Attributes:
    -----------
    tree : MentionTree
        The custom command tree used for handling interactions.

    Methods:
    --------
    __init__(intents: discord.Intents) -> None:
        Initializes the bot instance with the specified intents and configurations.

    setup_hook() -> None:
        Called when the bot logs in. Handles command synchronization and updates bot-related configurations.
    """

    def __init__(self, intents: discord.Intents) -> None:
        """
        Initializes the bot instance.

        Parameters:
        -----------
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

    async def setup_hook(self) -> None:
        """
        Called when the bot logs in.

        This method handles the synchronization of commands and updates bot-related configurations,
        such as the avatar URL and footer image.
        """
        synced_global = await self.tree.sync()
        cmds = len(synced_global)
        print(f"Synced {cmds} global commands.")

        if self.user.avatar:
            BotData.AVATAR_URL = self.user.avatar.url
        else:
            BotData.AVATAR_URL = None

        UtilConfig.FOOTER_IMAGE = BotData.AVATAR_URL
        print(f"\033[93m{self.user.name} has logged in successfully.\033[0m")
