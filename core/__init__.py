# This file initializes the `core` module and exposes the `Bot` class for external use.
# The `__all__` variable defines the public API of the module, restricting imports to the `Bot` class.

from core.bot import Bot

__all__ = ("Bot",)