from collections.abc import AsyncIterator, Generator
from logging import getLogger
from typing import Any, override

import discord
from discord import app_commands
from discord.ext import commands

__all__ = ("MentionTree",)
_log = getLogger(__name__)


class MentionTree(app_commands.CommandTree):
    """
    A custom command tree that stores and retrieves mentions for application commands.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the `MentionTree` instance with custom attributes for caching commands and mentions.

        Parameters
        ----------
        *args : Any
            Positional arguments passed to the parent class.
        **kwargs : Any
            Keyword arguments passed to the parent class.
        """
        super().__init__(*args, **kwargs)
        self.application_commands: dict[
            int | None, list[app_commands.AppCommand]
        ] = {}
        self.cache: dict[
            int | None,
            dict[
                app_commands.Command[Any, ..., Any]
                | commands.HybridCommand[Any, ..., Any]
                | str,
                str,
            ],
        ] = {}

    @override
    async def sync(
        self, *, guild: discord.abc.Snowflake | None = None
    ) -> list[app_commands.AppCommand]:
        """
        Synchronize commands and store them in the internal cache.

        Parameters
        ----------
        guild : Optional[discord.abc.Snowflake]
            The guild to synchronize commands for. If None, synchronizes global commands.

        Returns
        -------
        list[app_commands.AppCommand]
            The synchronized commands.
        """
        ret = await super().sync(guild=guild)
        guild_id = guild.id if guild else None
        self.application_commands[guild_id] = ret
        self.cache.pop(guild_id, None)
        return ret

    @override
    async def fetch_commands(
        self, *, guild: discord.abc.Snowflake | None = None
    ) -> list[app_commands.AppCommand]:
        """
        Fetch commands from Discord and update the internal cache.

        Parameters
        ----------
        guild : Optional[discord.abc.Snowflake]
            The guild to fetch commands for. If None, fetches global commands.

        Returns
        -------
        list[app_commands.AppCommand]
            The fetched commands.
        """
        ret = await super().fetch_commands(guild=guild)
        guild_id = guild.id if guild else None
        self.application_commands[guild_id] = ret
        self.cache.pop(guild_id, None)
        return ret

    async def get_or_fetch_commands(
        self, *, guild: discord.abc.Snowflake | None = None
    ) -> list[app_commands.AppCommand]:
        """
        Retrieve commands from the cache or fetch them if not available.

        Parameters
        ----------
        guild : Optional[discord.abc.Snowflake]
            The guild to retrieve commands for. If None, retrieves global commands.

        Returns
        -------
        list[app_commands.AppCommand]
            The retrieved or fetched commands.
        """
        try:
            return self.application_commands[guild.id if guild else None]
        except KeyError:
            return await self.fetch_commands(guild=guild)

    async def find_mention_for(
        self,
        command: app_commands.Command[Any, ..., Any]
        | commands.HybridCommand[Any, ..., Any]
        | str,
        *,
        guild: discord.abc.Snowflake | None = None,
    ) -> str | None:
        """
        Find the mention for a specific command, optionally scoped to a guild.

        Parameters
        ----------
        command : app_commands.Command | commands.HybridCommand | str
            The command to find the mention for.
        guild : Optional[discord.abc.Snowflake]
            The guild to scope the search to. If None, searches globally.

        Returns
        -------
        Optional[str]
            The mention for the command, if found.
        """
        guild_id = guild.id if guild else None
        try:
            return self.cache[guild_id][command]
        except KeyError:
            pass

        check_global = self.fallback_to_global is True and guild is not None

        if isinstance(command, str):
            _command = discord.utils.get(
                self.walk_commands(guild=guild), qualified_name=command
            )

            if check_global and not _command:
                _command = discord.utils.get(
                    self.walk_commands(), qualified_name=command
                )

        else:
            _command = command

        if not _command:
            return None

        local_commands = await self.get_or_fetch_commands(guild=guild)
        app_command_found = discord.utils.get(
            local_commands, name=(_command.root_parent or _command).name
        )

        if check_global and not app_command_found:
            global_commands = await self.get_or_fetch_commands(guild=None)
            app_command_found = discord.utils.get(
                global_commands, name=(_command.root_parent or _command).name
            )

        if not app_command_found:
            return None

        mention = f"</{_command.qualified_name}:{app_command_found.id}>"
        self.cache.setdefault(guild_id, {})
        self.cache[guild_id][command] = mention
        return mention

    def _walk_children(
        self,
        commands: list[
            app_commands.Group | app_commands.Command[Any, ..., Any]
        ],
    ) -> Generator[app_commands.Command[Any, ..., Any], None, None]:
        """
        Recursively iterate over child commands in a group.

        Parameters
        ----------
        commands : list[app_commands.Group | app_commands.Command]
            The list of commands to iterate over.

        Yields
        ------
        app_commands.Command
            The child commands.
        """
        for command in commands:
            if isinstance(command, app_commands.Group):
                yield from self._walk_children(command.commands)
            else:
                yield command

    async def walk_mentions(
        self, *, guild: discord.abc.Snowflake | None = None
    ) -> AsyncIterator[tuple[app_commands.Command[Any, ..., Any], str]]:
        """
        Retrieve all valid mentions for application commands in a specific guild.

        Parameters
        ----------
        guild : Optional[discord.abc.Snowflake]
            The guild to retrieve mentions for. If None, retrieves global mentions.

        Yields
        ------
        tuple[app_commands.Command, str]
            The command and its mention.
        """
        for command in self._walk_children(
            self.get_commands(
                guild=guild, type=discord.AppCommandType.chat_input
            )
        ):
            mention = await self.find_mention_for(command, guild=guild)
            if mention:
                yield command, mention
        if guild and self.fallback_to_global is True:
            for command in self._walk_children(
                self.get_commands(
                    guild=None, type=discord.AppCommandType.chat_input
                )
            ):
                mention = await self.find_mention_for(command, guild=guild)
                if mention:
                    yield command, mention
                else:
                    _log.warning(
                        "Could not find a mention for command %s in the API. Are you out of sync?",
                        command,
                    )
