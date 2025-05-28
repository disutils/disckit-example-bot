"""
This module serves as the entry point for the Discord bot application. It initializes the bot, configures its settings,
and starts the bot instance.

Functions:
----------
- load_cogs(bot: Bot) -> None:
    Loads cogs from the base cog directory.

- custom_status(bot: Bot) -> tuple[str, ...]:
    Defines custom status lines for the bot.

- main() -> None:
    Main entry point for the bot. Initializes and starts the bot instance.

Constants:
----------
- TOKEN: The Discord bot token retrieved from environment variables.
- intents: The Discord intents used by the bot for interacting with Discord.
"""

import asyncio
import logging
import os

import discord
import pyfiglet
from disckit import CogEnum, UtilConfig
from disckit.cogs import dis_load_extension
from dotenv import load_dotenv

from core import Bot
from core.config import (
    COG_DIR,
    ERROR_COLOR,
    FOOTER_TEXT,
    LOG_CHANNEL,
    MAIN_COLOR,
    SUCCESS_COLOR,
    BotData,
)
from core.emojis import GREEN_CHECK, RED_CROSS
from core.utils import setup_logging

# Load environment variables from a `.env` file
load_dotenv()

# Set up logging for the application
setup_logging()

logger = logging.getLogger(__name__)

# Retrieve the Discord bot token from the environment variables
TOKEN = os.getenv("TOKEN")

# Set up Discord intents for the bot
intents = discord.Intents.all()


async def load_cogs(bot: Bot) -> None:
    """
    Loads cogs from the base cog directory.

    Parameters:
    -----------
    bot : Bot
        The bot instance to load cogs into.
    """
    for folder in os.listdir(COG_DIR):
        for cog in os.listdir(COG_DIR + "/" + folder):
            if cog.endswith(".py"):
                cog_path = COG_DIR + "." + folder + "." + cog[:-3]
                await bot.load_extension(cog_path)


async def custom_status(bot: Bot) -> tuple[str, ...]:
    """
    Defines custom status lines for the bot.

    Parameters:
    -----------
    bot : Bot
        The bot instance.

    Returns:
    --------
    tuple[str, ...]
        A tuple containing custom status lines for the bot.
    """
    return (
        f"version {BotData.VERSION}",
        "Another Status Line Here",
        "Use /help for commands",
    )


async def main() -> None:
    """
    Main entry point for the bot.

    Initializes the bot instance, configures its settings, loads cogs, and starts the bot.
    """
    bot = Bot(intents=intents)

    # Set up Discord's internal logging
    discord.utils.setup_logging()

    # Display a banner for the bot
    print(pyfiglet.figlet_format("Disckit Example Bot"))

    # Configure utility settings for the bot
    UtilConfig.MAIN_COLOR = MAIN_COLOR
    UtilConfig.SUCCESS_COLOR = SUCCESS_COLOR
    UtilConfig.ERROR_COLOR = ERROR_COLOR

    UtilConfig.SUCCESS_EMOJI = GREEN_CHECK
    UtilConfig.ERROR_EMOJI = RED_CROSS

    UtilConfig.FOOTER_IMAGE = BotData.AVATAR_URL
    UtilConfig.FOOTER_TEXT = FOOTER_TEXT

    UtilConfig.STATUS_FUNC = (custom_status, ())
    UtilConfig.STATUS_TYPE = discord.ActivityType.listening
    UtilConfig.STATUS_COOLDOWN = 600

    UtilConfig.BUG_REPORT_CHANNEL = LOG_CHANNEL
    UtilConfig.OWNER_LIST_URL = (
        "https://images.disutils.com/bot_assets/assets/owners.txt"
    )

    # Load cogs and extensions
    await load_cogs(bot=bot)
    await dis_load_extension(
        bot, CogEnum.ERROR_HANDLER, CogEnum.STATUS_HANDLER
    )

    # Start the bot using the token
    await bot.start(TOKEN)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt detected.")
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
