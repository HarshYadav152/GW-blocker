# Installation Guide

Welcome to the installation guide for GW-Blocker! You can either download a pre-built binary for your operating system or build the application from source.

## Option 1: Download Pre-built Binary

> **Note:** Pre-built binaries are currently in progress. Please install from source.

### Windows
1. Download the latest `.exe` file from the [Releases page](https://github.com/HarshYadav152/GW-blocker/releases).
2. Right-click the downloaded file and select **"Run as administrator"**.

### macOS
1. Download the latest `.dmg` file from the [Releases page](https://github.com/HarshYadav152/GW-blocker/releases).
2. Open the `.dmg` file and drag the application to your Applications folder.
3. When running for the first time, right-click on the app and select **"Open"**.
4. Enter your password when prompted.

### Linux
1. Download the appropriate package for your distribution from the [Releases page](https://github.com/HarshYadav152/GW-blocker/releases).
   - `.deb` for Debian/Ubuntu-based distributions
   - `.rpm` for Fedora/RHEL-based distributions
   - `.AppImage` for universal use
2. Make the file executable and run it:
   ```bash
   chmod +x WebsiteBlocker-*.AppImage
   ./WebsiteBlocker-*.AppImage
   ```

## Option 2: Install from Source

If you prefer to run the script directly using Python, follow these steps:

### Requirements
- Python 3.6 or higher
- `tkinter` (usually included with Python)
- `pip` (Python package installer)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HarshYadav152/GW-blocker.git
   cd GW-blocker
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   Since GW-Blocker modifies the system's `hosts` file, it requires administrator or root privileges.

   **Windows:**
   - Open Command Prompt as Administrator.
   - Navigate to the project directory:
     ```bash
     cd path\to\GW-blocker
     python -m src.main
     ```

   **macOS / Linux:**
   - Run the script with `sudo`:
     ```bash
     sudo python3 -m src.main
     ```

4. **Verify dependencies**:
   - Make sure you are running Python 3.6 or later.
   - Ensure `tkinter` is installed and available in the active Python environment.
   - If `tkinter` is missing, install it through your package manager or use a Python distribution that includes it.

