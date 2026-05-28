# Architecture Overview

GW-Blocker is a lightweight desktop application built using Python. It relies on the built-in `tkinter` library for the graphical user interface (GUI) and interacts directly with the operating system's `hosts` file to block domains.

## Core Components

The application is structured into three main components:

1. **User Interface (`src/gui.py`)**
   - Built using `tkinter`.
   - Handles user input, such as entering URLs and selecting blocking durations.
   - Displays the list of currently blocked websites.
   - Triggers calls to the blocker module.

2. **Core Blocker Logic (`src/blocker.py`)**
   - The heart of the application, encapsulated in the `WebsiteBlocker` class.
   - Determines the appropriate `hosts` file location based on the operating system (`C:\Windows\System32\drivers\etc\hosts` for Windows, `/etc/hosts` for Unix systems).
   - Manages elevated privileges, checking if the script is running as Administrator/root.
   - Implements methods to append domains to the `hosts` file (mapping them to `127.0.0.1`) and remove them when unblocked.

3. **Utilities (`src/utils.py`)**
   - Helper functions for URL validation and normalization (`clean_url`, `is_valid_url`).
   - Configuration management to persist block lists and block durations to `~/.website_blocker/config.json`.

## Data Flow

1. User enters a URL (e.g., `facebook.com`) in the GUI.
2. The GUI uses `utils.py` to validate and clean the URL.
3. The GUI calls `blocker.block_website(url)`.
4. `blocker.py` verifies admin privileges and writes `127.0.0.1 facebook.com` to the system's `hosts` file.
5. The state is updated, and the new configuration is written to the local config file by `utils.py`.
