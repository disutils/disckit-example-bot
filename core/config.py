from discord import utils


class BotData:
    """
    Contains metadata and dynamic properties related to the bot.

    Attributes
    ----------
    VERSION : str
        The current version of the bot.
    SUPPORT_SERVER : str
        Link to the support server.
    REPO_URL : str
        The GitHub repository URL for version checking.
    AVATAR_URL : str or None
        Optional URL for the bot's avatar.
    """

    VERSION: str = "1.0.2"  # The current version of the bot (currently based on the latest version of disckit)
    SUPPORT_SERVER: str = (
        "https://discord.gg/28RuT8WsKT"  # Link to the support server
    )
    REPO_URL: str = "https://github.com/disutils/disckit-example-bot"  # GitHub repository URL
    AVATAR_URL: str | None = None  # Optional URL for the bot's avatar


# Ownership and Permissions
OWNER_IDS: set[int] = {
    418941954252996609,  # RejectModders
    1022085572719808542,  # Jiggly Balls
}  # A set of user IDs for the bot's owners


# Embed Configuration
FOOTER_TEXT: str = f"Powered by © Disutils Team 2024-{utils.utcnow().year}"  # Footer text for embeds, dynamically includes the current year

# Embed Colors
MAIN_COLOR: int = 0x5865F2  # Main color for embeds (Discord blurple)
SUCCESS_COLOR: int = 0x00FF00  # Success color for embeds (green)
ERROR_COLOR: int = 0xFF0000  # Error color for embeds (red)


# Cog Configuration
COG_DIR: str = "cogs"  # The base directory of the cogs to be loaded


# Logging Configuration
LOG_DIR: str = "logs"  # The base directory of the logs to be stored
LOG_FILE: str = "bot.log"  # The name of the log file
MAX_LOGS: int = 10  # The maximum number of logs to store
MAX_LOG_SIZE: int = 5 * 1024 * 1024  # Maximum log file size (5 MB)
LOG_LEVEL: str = "INFO"  # The logging level for the application
LOG_DEBUG: bool = False  # A flag to enable or disable debug mode


# Log Channel
LOG_CHANNEL: int = 1234  # Replace with the actual channel ID
