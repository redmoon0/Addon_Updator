# addon_updater.py
"""
Addon Updater Utility
Provides functions to check GitHub for addon updates.
Supports public & private repos via GitHub personal access tokens.
"""

import requests
from typing import Optional, Tuple


def get_latest_version(
    owner: str,
    repo: str,
    use_releases: bool = True,
    branch: str = "main",
    token: Optional[str] = None
) -> Optional[Tuple[int, int, int]]:
    """
    Query GitHub API to fetch the latest release or branch tag.
    :param owner: GitHub username or organization.
    :param repo: Repository name.
    :param use_releases: Whether to fetch latest release (True) or branch reference (False).
    :param branch: Branch name to check if use_releases=False.
    :param token: GitHub Personal Access Token (optional, needed for private repos).
    :return: Tuple of (major, minor, patch) or None if error.
    """
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    api_url = (
        f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        if use_releases else
        f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{branch}"
    )

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        version_str = (
            data["tag_name"] if use_releases else data["object"]["sha"][:7]
        )
        return parse_version_string(version_str)
    except Exception as e:
        print(f"[Addon Updater] Error fetching latest version: {e}")
        return None


def parse_version_string(tag: str) -> Optional[Tuple[int, int, int]]:
    """
    Parses a version-like tag into (major, minor, patch).
    Supports formats: 'v1.2.3' or '1.2.3'
    """
    import re
    match = re.match(r"v?(\d+)\.(\d+)\.(\d+)", tag)
    if match:
        return tuple(map(int, match.groups()))
    return None


def is_newer_version(
    current: Tuple[int, int, int], latest: Tuple[int, int, int]
) -> bool:
    """
    Compare current vs latest version.
    Returns True if latest > current.
    """
    return latest > current


# Optional: test utility when running standalone
if __name__ == "__main__":
    # Example test
    owner = "octocat"
    repo = "Hello-World"
    print("Latest version:", get_latest_version(owner, repo))
