# Internal API Documentation

Since GW-Blocker is a desktop application, it does not expose a traditional REST API over the network. However, the internal Python components are structured cleanly, making it easy to integrate or extend.

## `src.blocker.WebsiteBlocker`

The core class responsible for handling system-level file modifications.

### Methods

- **`__init__()`**
  Initializes the `hosts` file path based on the operating system.

- **`is_admin() -> bool`**
  Checks whether the application was launched with administrator (Windows) or root (macOS/Linux) privileges.

- **`block_website(website: str) -> bool`**
  Blocks a single domain by redirecting it to `127.0.0.1` in the `hosts` file. Returns `True` on success.

- **`block_websites(websites: List[str]) -> bool`**
  Blocks a list of domains. Returns `True` on success.

- **`unblock_website(website: str) -> bool`**
  Removes a specific domain from the `hosts` file. Returns `True` on success.

- **`unblock_all() -> bool`**
  Removes all custom entries (redirects to `127.0.0.1`) made by the application from the `hosts` file.

- **`get_blocked_websites() -> List[str]`**
  Parses the `hosts` file and returns a list of all currently blocked domains.

## `src.utils`

Helper functions for string manipulation and configuration management.

- **`is_valid_url(url: str) -> bool`**
  Validates if the string matches a basic domain format.

- **`clean_url(url: str) -> str`**
  Strips `http://`, `https://`, `www.`, and query strings to return a clean domain name.

- **`load_config() -> Dict[str, Any]`**
  Loads application settings and the saved list of blocked sites from `~/.website_blocker/config.json`.

- **`save_blocked_sites(sites: List[str]) -> bool`**
  Persists the list of blocked domains to the local configuration file.

- **`save_block_until(timestamp: Optional[str]) -> bool`**
  Saves a specific ISO timestamp indicating when temporary blocks should expire.
