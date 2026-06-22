import re
import json
import os
import hmac
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List

# Create user config directory
CONFIG_DIR = Path(os.path.expanduser("~")) / ".website_blocker"
CONFIG_DIR.mkdir(exist_ok=True)
CONFIG_FILE = CONFIG_DIR / "config.json"

def is_valid_url(url: str) -> bool:
    """Check if the given string is a valid URL format."""
    # Simple URL validation - checks for domain format
    pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, url))

def clean_url(url: str) -> str:
    """Clean and normalize a URL."""
    # Remove http://, https://, and www. prefixes
    url = re.sub(r'^https?://', '', url)
    url = re.sub(r'^www\.', '', url)
    # Remove paths, query strings, etc.
    url = url.split('/')[0]
    return url.lower()

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


# ---------------------------------------------------------------------------
# Import / Export helpers (issue #7)
# ---------------------------------------------------------------------------

EXPORT_FORMAT_VERSION = 1


def build_export_data(blocked_sites: List[str], config: Dict[str, Any]) -> Dict[str, Any]:
    """Build the JSON-serialisable structure for an exported block list.

    The app tracks a single global ``block_until`` rather than per-domain
    expiry, so each site entry reflects that shared schedule. This keeps the
    export faithful to the application's real state while still recording the
    domain, block type, and expiry the issue asks for.
    """
    block_until = config.get("block_until")
    block_type = "timed" if block_until else "permanent"

    sites = []
    for domain in blocked_sites:
        sites.append({
            "domain": domain,
            "block_type": block_type,
            "expiry": block_until,  # ISO string when timed, else None
        })

    return {
        "format": "gw-blocker-blocklist",
        "version": EXPORT_FORMAT_VERSION,
        "block_until": block_until,
        "sites": sites,
    }


def _extract_import_entries(raw: Any) -> List[Any]:
    """Pull candidate entries out of a parsed import object.

    Accepts several shapes for resilience:
      * the rich export dict ({"sites": [{"domain": ...}, ...]})
      * a bare list of domain strings (["a.com", "b.com"])
      * a list of dicts ([{"domain": "a.com"}, ...])
      * a dict with a "blocked_sites" list (the app's own config shape)

    Returns the raw candidate values (strings, or the domain field of dicts).
    Non-string domain fields are returned as-is so the caller can report them
    as skipped rather than silently dropping them.
    """
    candidates: List[Any] = []

    def take(entry):
        if isinstance(entry, dict):
            candidates.append(entry.get("domain"))
        else:
            candidates.append(entry)

    if isinstance(raw, dict):
        if isinstance(raw.get("sites"), list):
            for entry in raw["sites"]:
                take(entry)
        elif isinstance(raw.get("blocked_sites"), list):
            for entry in raw["blocked_sites"]:
                take(entry)
    elif isinstance(raw, list):
        for entry in raw:
            take(entry)

    return candidates


def parse_import_data(raw: Any):
    """Validate and normalise domains from a parsed import object.

    Returns a tuple ``(valid_domains, skipped)`` where ``valid_domains`` is a
    de-duplicated list of clean, valid domains (order preserved) and
    ``skipped`` is a list of the raw entries that were invalid or unparseable.
    """
    valid: List[str] = []
    skipped: List[str] = []
    seen = set()

    for candidate in _extract_import_entries(raw):
        if isinstance(candidate, str):
            # Lower-case first so uppercase schemes (HTTP://) are handled by
            # clean_url, which only strips lowercase http(s):// and www.
            cleaned = clean_url(candidate.strip().lower())
            if cleaned and is_valid_url(cleaned):
                if cleaned not in seen:
                    seen.add(cleaned)
                    valid.append(cleaned)
                continue
        skipped.append(str(candidate))

    return valid, skipped


# ---------------------------------------------------------------------------
# Password protection (issue #5)
# ---------------------------------------------------------------------------
#
# The password is never stored in plain text. We derive a key with
# PBKDF2-HMAC-SHA256 over a fresh random salt and a high iteration count, and
# store only {algo, salt, hash, iterations}. Verification recomputes the key
# from the candidate password and compares it in constant time. All of this
# uses the standard library (hashlib, hmac, os) -- no new dependencies.

_PBKDF2_ALGO = "pbkdf2_sha256"
_PBKDF2_ITERATIONS = 200_000
_SALT_BYTES = 16


def hash_password(password: str) -> Dict[str, Any]:
    """Hash a password with PBKDF2-HMAC-SHA256 and a fresh random salt.

    Returns a JSON-serialisable record. The plain password is never returned
    or stored -- only the salt, the derived hash, and the parameters needed to
    verify a future candidate.
    """
    salt = os.urandom(_SALT_BYTES)
    derived = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, _PBKDF2_ITERATIONS
    )
    return {
        "algo": _PBKDF2_ALGO,
        "salt": salt.hex(),
        "hash": derived.hex(),
        "iterations": _PBKDF2_ITERATIONS,
    }


def verify_password_hash(stored: Optional[Dict[str, Any]], password: str) -> bool:
    """Constant-time check of a candidate password against a stored record.

    Returns False if there is no stored record or it is malformed, so a corrupt
    config can never be treated as "no password set" by a caller that only
    checks this function.
    """
    if not stored:
        return False
    try:
        salt = bytes.fromhex(stored["salt"])
        expected = bytes.fromhex(stored["hash"])
        iterations = int(stored.get("iterations", _PBKDF2_ITERATIONS))
    except (KeyError, ValueError, TypeError):
        return False
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(derived, expected)


def is_password_set() -> bool:
    """True if a password hash is configured."""
    return bool(load_config().get("password"))


def set_password(password: str) -> bool:
    """Store a new password (hashed). Overwrites any existing one."""
    try:
        config = load_config()
        config["password"] = hash_password(password)
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception:
        return False


def verify_password(password: str) -> bool:
    """Verify a candidate password against the stored hash.

    Returns True when no password is configured, so callers that gate an action
    can simply do ``if not verify_password(...)`` once they know protection is
    on. Use is_password_set() to decide whether to prompt at all.
    """
    stored = load_config().get("password")
    if not stored:
        return True
    return verify_password_hash(stored, password)


def remove_password() -> bool:
    """Remove the stored password hash, disabling protection."""
    try:
        config = load_config()
        config.pop("password", None)
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception:
        return False
