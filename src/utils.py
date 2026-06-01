import re
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List

# Create user config directory
CONFIG_DIR = Path(os.path.expanduser("~")) / ".website_blocker"
CONFIG_DIR.mkdir(exist_ok=True)
CONFIG_FILE = CONFIG_DIR / "config.json"

def is_valid_url(url: str) -> bool:
    """Check if the given string is a valid domain name."""
    url = url.strip().lower()
    if not url or url.startswith("http://") or url.startswith("https://"):
        return False

    # Basic domain validation: labels separated by dots, no spaces or unsafe characters.
    pattern = r'^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$'
    return bool(re.match(pattern, url))


def clean_url(url: str) -> str:
    """Clean and normalize a URL to a bare domain name."""
    url = url.strip().lower()
    # Remove scheme and common prefixes
    url = re.sub(r'^https?://', '', url)
    url = re.sub(r'^www\.', '', url)
    # Remove any path, query string, or fragment data
    url = re.split(r'[/?#]', url, maxsplit=1)[0]
    return url
def save_blocked_sites(sites: List[str]) -> bool:
    """Save list of blocked sites to config file."""
    try:
        config = load_config()
        config["blocked_sites"] = sites
        
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception:
        return False

def load_config() -> Dict[str, Any]:
    """Load application configuration."""
    default_config = {
        "blocked_sites": [],
        "block_until": None
    }
    
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        return default_config
    except Exception:
        return default_config

def save_block_until(timestamp: Optional[str]) -> bool:
    """Save block until timestamp."""
    try:
        config = load_config()
        config["block_until"] = timestamp
        
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception:
        return False