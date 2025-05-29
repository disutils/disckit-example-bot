"""
This module defines configuration constants and classes for the Discord bot.

Classes:
--------
- BotData: Contains metadata and dynamic properties related to the bot.

Constants:
----------
- OWNER_IDS: A set of user IDs for the bot's owners.
- FOOTER_TEXT: Footer text for embeds, dynamically includes the current year.
- COG_DIR: The base directory of the cogs to be loaded.
- LOG_DIR: The base directory of the logs to be stored.
- LOG_FILE: The name of the log file.
- MAX_LOGS: The maximum number of logs to store.
- MAX_LOG_SIZE: Maximum log file size (5 MB).
- LOG_CHANNEL: Channel ID for general logs.
- MAIN_COLOR: Main color for embeds (blue).
- SUCCESS_COLOR: Success color for embeds (green).
- ERROR_COLOR: Error color for embeds (red).
"""

from discord import utils


class BotData:
    """
    Contains metadata and dynamic properties related to the bot.

    Attributes:
    -----------
    VERSION : str
        The current version of the bot.
    SUPPORT_SERVER : str
        Link to the support server.
    AVATAR_URL : Optional[str]
        Optional URL for the bot's avatar.
    """

    VERSION: str = "0.9"  # The current version of the bot (in this case its based on Disckit)
    SUPPORT_SERVER: str = (
        "https://discord.gg/28RuT8WsKT"  # Link to the support server
    )
    AVATAR_URL: str | None = None  # Optional URL for the bot's avatar


OWNER_IDS: set[int] = {
    418941954252996609,  # RejectModders
    1022085572719808542,  # Jiggly Balls
}  # A set of user IDs for the bot's owners

FOOTER_TEXT: str = f"Powered by © Disutils Team 2024-{utils.utcnow().year}"  # Footer text for embeds, dynamically includes the current year
COG_DIR: str = "cogs"  # The base directory of the cogs to be loaded
LOG_DIR: str = "logs"  # The base directory of the logs to be stored
LOG_FILE: str = "bot.log"  # The name of the log file
MAX_LOGS: int = 10  # The maximum number of logs to store
MAX_LOG_SIZE: int = 5 * 1024 * 1024  # Maximum log file size (5 MB)

LOG_CHANNEL: int = 123456789012345678  # Replace with the actual channel ID

# Colours -
MAIN_COLOR: int = 0x5865F2  # Main color for embeds (blue)
SUCCESS_COLOR: int = 0x00FF00  # Success color for embeds (green)
ERROR_COLOR: int = 0xFF0000  # Error color for embeds (red)
