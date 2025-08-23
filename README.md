# GW-Blocker GUI

A lightweight, cross-platform application that blocks distracting websites by modifying your system's hosts file.

GW-Blocker Screenshot
<img src="https://raw.githubusercontent.com/HarshYadav152/resources/main/images/GW-blocker/gwblocker.png"/>

## Features

- Simple, intuitive interface for blocking and unblocking websites
- Block websites permanently or until a specific time
- Cross-platform: works on Windows, macOS, and Linux
- No internet connection required (works completely offline)
- Open source and free to use

## Installation

### Option 1: Download Pre-built Binary (in progress try from using source)

#### Windows
1. Download the latest `.exe` file from the [Releases page](https://github.com/HarshYadav152/GW-blocker/releases)
2. Right-click the downloaded file and select "Run as administrator"

#### macOS
1. Download the latest `.dmg` file from the [Releases page](https://github.com/HarshYadav152/GW-blocker/releases)
2. Open the .dmg file and drag the application to your Applications folder
3. When running for the first time, right-click on the app and select "Open"
4. Enter your password when prompted

#### Linux
1. Download the appropriate package for your distribution from the [Releases page](https://github.com/HarshYadav152/GW-blocker/releases)
   - `.deb` for Debian/Ubuntu-based distributions
   - `.rpm` for Fedora/RHEL-based distributions
   - `.AppImage` for universal use
2. Make the file executable:
```bash
chmod +x WebsiteBlocker-*.AppImage
```

### Option 2: Install from Source (working)

#### Requirements
- Python 3.6 or higher
- Tkinter (usually included with Python)

#### Steps
1. Clone the repository:
```bash
git clone https://github.com/HarshYadav152/GW-blocker.git
cd GW-blocker
```


2. Install dependencies:
```python
pip install -r requirements.txt
```

3. Run the application with administrator/root privileges:

**Windows**:
- Right-click Command Prompt and select "Run as administrator"
- Navigate to the project directory:
  ``` bash
  cd path\to\GW-blocker
  python -m src.main
  ```

**macOS/Linux**:
```bash
sudo python3 -m src.main
```


## Usage

1. **Adding a website to block**:
- Enter the domain name (e.g., `facebook.com`) in the URL field
- Select block duration (permanent or until specific time)
- Click "Block"

2. **Unblocking websites**:
- Select a website from the list
- Click "Unblock Selected" to remove individual sites
- Or click "Unblock All" to remove all blocks

3. **Setting a time limit**:
- Choose "Until" option
- Set the desired time
- Website will be automatically unblocked after that time

## Why Administrator/Root Privileges?

This application modifies your system's hosts file, which requires elevated permissions on all operating systems. The hosts file is a protected system file that maps hostnames to IP addresses.

## Building from Source

### Windows
```bash
pip install pyinstaller pyinstaller --onefile --windowed --uac-admin --icon=assets/icon.ico --name <app-name> src/main.py
```
### macOS
```bash
pip install pyinstaller pyinstaller --onefile --windowed --icon=assets/icon.icns --name <app-name> src/main.py
```
### Linux
```bash
pip install pyinstaller pyinstaller --onefile --name <app-name> src/main.py
```

#### change <app-name> to any name of the app
