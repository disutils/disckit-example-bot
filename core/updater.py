import asyncio
import logging
import re
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

import aiohttp
from packaging import version
from packaging.version import InvalidVersion

from core.config import BotData

_logger = logging.getLogger(__name__)


class UpdateStatus(Enum):
    """Enumeration of possible update statuses."""

    UP_TO_DATE = "up_to_date"
    OUTDATED = "outdated"
    AHEAD = "ahead"
    ERROR = "error"
    FETCH_FAILED = "fetch_failed"
    INVALID_VERSION = "invalid_version"


class ColorCode(Enum):
    """ANSI color codes for terminal output."""

    GREEN = "\033[92m"  # Success/Up to date
    RED = "\033[91m"  # Error/Outdated
    BLUE = "\033[94m"  # Info/URLs
    PURPLE = "\033[95m"  # Ahead version
    CYAN = "\033[96m"  # General info
    WHITE = "\033[97m"  # Neutral
    RESET = "\033[0m"  # Reset color


@dataclass
class ReleaseInfo:
    """Data class for GitHub release information."""

    tag_name: str
    name: str
    html_url: str
    published_at: str
    body: str

    @property
    def truncated_body(self) -> str:
        """Get truncated release notes."""
        if len(self.body) > 500:
            return self.body[:500] + "..."
        return self.body


@dataclass
class VersionComparison:
    """Data class for version comparison results."""

    status: UpdateStatus
    message: str
    current_version: str
    latest_version: str
    current_normalized: str
    latest_normalized: str
    release_info: ReleaseInfo | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for backward compatibility."""
        result = {
            "status": self.status.value,
            "message": self.message,
            "current_version": self.current_version,
            "latest_version": self.latest_version,
            "current_normalized": self.current_normalized,
            "latest_normalized": self.latest_normalized,
        }

        if self.release_info:
            result.update(
                {
                    "release_name": self.release_info.name,
                    "release_url": self.release_info.html_url,
                    "release_date": self.release_info.published_at,
                    "release_notes": self.release_info.truncated_body,
                }
            )

        return result


class GitHubAPIError(Exception):
    """Custom exception for GitHub API related errors."""

    pass


class VersionParsingError(Exception):
    """Custom exception for version parsing errors."""

    pass


class GitHubReleaseChecker:
    """
    Enhanced GitHub release checker with improved error handling and type safety.
    """

    def __init__(self, timeout: int = 10, max_retries: int = 3) -> None:
        """
        Initialize the GitHub release checker.

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.repo_url: str = BotData.REPO_URL.rstrip("/")
        self.api_url: str = self._convert_to_api_url(self.repo_url)
        self.timeout: aiohttp.ClientTimeout = aiohttp.ClientTimeout(
            total=timeout
        )
        self.max_retries: int = max_retries

    def _convert_to_api_url(self, repo_url: str) -> str:
        """
        Convert a GitHub repository URL to the API URL for releases.

        Args:
            repo_url: The GitHub repository URL

        Returns:
            The GitHub API URL for releases

        Raises:
            GitHubAPIError: If the URL format is invalid
        """
        patterns = [
            r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?/?$",
            r"^([^/]+)/([^/]+)$",  # Short format: owner/repo
        ]

        for pattern in patterns:
            match = re.search(pattern, repo_url)
            if match:
                owner, repo = match.groups()
                api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
                return api_url

        raise GitHubAPIError(f"Invalid GitHub URL format: {repo_url}")

    @asynccontextmanager
    async def _get_session(
        self,
    ) -> AsyncGenerator[aiohttp.ClientSession, None]:
        """Context manager for aiohttp session."""
        async with aiohttp.ClientSession(
            timeout=self.timeout,
            headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": f"GitHubReleaseChecker/1.0 ({BotData.REPO_URL})",
            },
        ) as session:
            yield session

    async def _fetch_with_retry(self, url: str) -> dict[str, Any] | None:
        """
        Fetch data from URL with retry logic.

        Args:
            url: The URL to fetch

        Returns:
            JSON response data or None if all attempts failed
        """
        last_exception: GitHubAPIError | None = None

        for attempt in range(self.max_retries):
            try:
                async with self._get_session() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            return data
                        elif response.status == 404:
                            raise GitHubAPIError(
                                "Repository not found or no releases available (HTTP 404)"
                            )
                        elif response.status == 403:
                            raise GitHubAPIError(
                                "API rate limit exceeded (HTTP 403)"
                            )
                        else:
                            raise GitHubAPIError(
                                f"HTTP {response.status}: {response.reason}"
                            )

            except asyncio.TimeoutError as e:
                last_exception = GitHubAPIError(
                    f"Request timeout after {self.timeout.total}s"
                )
                _logger.warning(f"Timeout on attempt {attempt + 1}: {e}")
            except aiohttp.ClientError as e:
                last_exception = GitHubAPIError(f"Network error: {e}")
                _logger.warning(f"Network error on attempt {attempt + 1}: {e}")
            except Exception as e:
                last_exception = GitHubAPIError(f"Unexpected error: {e}")
                _logger.error(
                    f"Unexpected error on attempt {attempt + 1}: {e}"
                )

            if attempt < self.max_retries - 1:
                await asyncio.sleep(2**attempt)  # Exponential backoff

        _logger.error(
            f"All {self.max_retries} attempts failed. Last error: {last_exception}"
        )
        if last_exception is not None:
            raise last_exception
        else:
            raise GitHubAPIError("All retry attempts failed")

    async def get_latest_release(self) -> ReleaseInfo | None:
        """
        Fetch the latest release information from GitHub API.

        Returns:
            ReleaseInfo object or None if fetch failed

        Raises:
            GitHubAPIError: If API request fails
        """
        try:
            data = await self._fetch_with_retry(self.api_url)
            if not data:
                return None

            return ReleaseInfo(
                tag_name=data.get("tag_name", "unknown"),
                name=data.get("name", ""),
                html_url=data.get("html_url", ""),
                published_at=data.get("published_at", ""),
                body=data.get("body", ""),
            )

        except GitHubAPIError:
            raise
        except Exception as e:
            raise GitHubAPIError(f"Failed to parse release data: {e}")

    def _normalize_version(self, version_str: str) -> str:
        """
        Normalize version string by removing common prefixes and cleaning format.

        Args:
            version_str: The version string to normalize

        Returns:
            The normalized version string
        """
        if not version_str or not isinstance(version_str, str):
            return "0.0.0"

        # Remove common prefixes
        normalized = re.sub(
            r"^(v|version|release|tag)[\s\-_]*",
            "",
            version_str.strip(),
            flags=re.IGNORECASE,
        )

        # Clean up any remaining non-version characters at the start
        normalized = re.sub(r"^[^\d]*", "", normalized)

        # If empty after cleanup, return default
        if not normalized:
            return "0.0.0"

        return normalized

    def compare_versions(
        self, current_version: str, release_info: ReleaseInfo
    ) -> VersionComparison:
        """
        Compare current version with latest version.

        Args:
            current_version: The current bot version
            release_info: Release information from GitHub

        Returns:
            VersionComparison object with comparison results
        """
        try:
            current_norm = self._normalize_version(current_version)
            latest_norm = self._normalize_version(release_info.tag_name)

            current_ver = version.parse(current_norm)
            latest_ver = version.parse(latest_norm)

            if current_ver < latest_ver:
                status = UpdateStatus.OUTDATED
                message = f"🔴 Oh no! The bot's living in the past. Current: v{current_version}, Latest: {release_info.tag_name}"
            elif current_ver > latest_ver:
                status = UpdateStatus.AHEAD
                message = f"🟣 Time traveler detected! The bot's from the future. Current: v{current_version}, Latest: {release_info.tag_name}"
            else:
                status = UpdateStatus.UP_TO_DATE
                message = f"🟢 All systems go! The bot is as fresh as it gets. Version: v{current_version}"

            return VersionComparison(
                status=status,
                message=message,
                current_version=current_version,
                latest_version=release_info.tag_name,
                current_normalized=current_norm,
                latest_normalized=latest_norm,
                release_info=release_info,
            )

        except InvalidVersion as e:
            _logger.error(f"Invalid version format: {e}")
            return VersionComparison(
                status=UpdateStatus.INVALID_VERSION,
                message=f"❌ Invalid version format: {e}",
                current_version=current_version,
                latest_version=release_info.tag_name,
                current_normalized="",
                latest_normalized="",
                release_info=release_info,
            )
        except Exception as e:
            _logger.error(f"Error comparing versions: {e}")
            return VersionComparison(
                status=UpdateStatus.ERROR,
                message=f"❌ Error comparing versions: {e}",
                current_version=current_version,
                latest_version=release_info.tag_name,
                current_normalized="",
                latest_normalized="",
                release_info=release_info,
            )

    async def check_for_updates(self) -> VersionComparison:
        """
        Check if the bot is up to date with the latest GitHub release.

        Returns:
            VersionComparison object with update check results
        """
        try:
            release_info = await self.get_latest_release()

            if not release_info:
                return VersionComparison(
                    status=UpdateStatus.FETCH_FAILED,
                    message="❌ Failed to fetch release information from GitHub",
                    current_version=BotData.VERSION,
                    latest_version="unknown",
                    current_normalized="",
                    latest_normalized="",
                )

            return self.compare_versions(BotData.VERSION, release_info)

        except GitHubAPIError as e:
            _logger.error(f"GitHub API error: {e}")
            return VersionComparison(
                status=UpdateStatus.ERROR,
                message=f"❌ GitHub API error: {e}",
                current_version=BotData.VERSION,
                latest_version="unknown",
                current_normalized="",
                latest_normalized="",
            )
        except Exception as e:
            _logger.error(f"Unexpected error during update check: {e}")
            return VersionComparison(
                status=UpdateStatus.ERROR,
                message=f"❌ Unexpected error: {e}",
                current_version=BotData.VERSION,
                latest_version="unknown",
                current_normalized="",
                latest_normalized="",
            )


def _print_colored(message: str, color: ColorCode) -> None:
    """Print a colored message to the console."""
    print(f"{color.value}{message}{ColorCode.RESET.value}")


def _format_date(iso_date_string: str) -> str:
    """
    Convert ISO date string to friendly date format.

    Args:
        iso_date_string: ISO format date string (e.g., "2025-06-01T09:11:43Z")

    Returns:
        Formatted date string (e.g., "6/1/2025")
    """
    if not iso_date_string:
        return "Unknown"

    try:
        # Parse ISO format and convert to friendly date
        dt = datetime.fromisoformat(iso_date_string.replace("Z", "+00:00"))
        return dt.strftime("%-m/%-d/%Y")  # Remove leading zeros (Unix/macOS)
    except (ValueError, AttributeError):
        try:
            # Fallback for Windows (doesn't support -)
            dt = datetime.fromisoformat(iso_date_string.replace("Z", "+00:00"))
            return dt.strftime("%m/%d/%Y").lstrip("0").replace("/0", "/")
        except ValueError:
            return "Invalid Date"


async def check_bot_updates() -> None:
    """
    Check for bot updates and display the result with colored output.
    """
    try:
        _print_colored("🔍 Checking for updates...", ColorCode.CYAN)

        checker = GitHubReleaseChecker()
        result = await checker.check_for_updates()

        # Print main status message with appropriate color
        if result.status == UpdateStatus.UP_TO_DATE:
            _print_colored(result.message, ColorCode.GREEN)
        elif result.status == UpdateStatus.OUTDATED:
            _print_colored(result.message, ColorCode.RED)
        elif result.status == UpdateStatus.AHEAD:
            _print_colored(result.message, ColorCode.PURPLE)
        else:
            _print_colored(result.message, ColorCode.RED)

        # Print additional information
        if result.release_info and result.release_info.html_url:
            _print_colored(
                f"🔗 Release URL: {result.release_info.html_url}",
                ColorCode.BLUE,
            )

            if result.release_info.name:
                _print_colored(
                    f"📋 Release Name: {result.release_info.name}",
                    ColorCode.WHITE,
                )

            if result.release_info.published_at:
                formatted_date = _format_date(result.release_info.published_at)
                _print_colored(
                    f"📅 Published: {formatted_date}",
                    ColorCode.CYAN,
                )

    except Exception as e:
        error_msg = f"❌ Failed to check for updates: {e}"
        _print_colored(error_msg, ColorCode.RED)
        _logger.error(error_msg)
