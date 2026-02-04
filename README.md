# GW-Blocker GUI

![License](https://img.shields.io/github/license/HarshYadav152/GW-blocker)
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

A lightweight, cross-platform application that blocks distracting websites by modifying your system's hosts file.

![GW-Blocker Screenshot](https://raw.githubusercontent.com/HarshYadav152/resources/main/images/GW-blocker/gwblocker.png)

## Features

- ✨ Simple, intuitive interface for blocking and unblocking websites
- ⏰ Block websites permanently or until a specific time
- 🌍 Cross-platform: works on Windows, macOS, and Linux
- 🔒 No internet connection required (works completely offline)
- 📖 Open source and free to use

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Building from Source](#building-from-source)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Installation

### Option 1: Download Pre-built Binary

> **Note:** Pre-built binaries are currently in progress. Please install from source.

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
./WebsiteBlocker-*.AppImage
```

### Option 2: Install from Source

#### Requirements
- Python 3.6 or higher
- Tkinter (usually included with Python)
- pip (Python package installer)

#### Steps
1. Clone the repository:
```bash
git clone https://github.com/HarshYadav152/GW-blocker.git
cd GW-blocker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application with administrator/root privileges:

**Windows**:
- Right-click Command Prompt and select "Run as administrator"
- Navigate to the project directory:
```bash
cd path\to\GW-blocker
python -m src.main
```

**macOS/Linux**:
```bash
sudo python3 -m src.main
```

## Usage

### Blocking a Website

1. Enter the domain name (e.g., `facebook.com`) in the URL field
2. Select block duration:
   - **Permanent**: Block indefinitely until manually unblocked
   - **Until**: Block until a specific time
3. Click **"Block"**

### Unblocking Websites

- **Unblock Selected**: Select a website from the list and click this button
- **Unblock All**: Remove all blocks at once

### Setting Time-Based Blocks

1. Choose **"Until"** option
2. Set the desired time using the time picker
3. The website will be automatically unblocked after that time

## Why Administrator/Root Privileges?

This application modifies your system's hosts file, which requires elevated permissions on all operating systems. The hosts file is a protected system file that maps hostnames to IP addresses. By redirecting blocked domains to `127.0.0.1` (localhost), the application prevents your browser from accessing those sites.

## Building from Source

### Prerequisites
```bash
pip install pyinstaller
```

### Windows
```bash
pyinstaller --onefile --windowed --uac-admin --icon=assets/icon.ico --name GW-Blocker src/main.py
```

### macOS
```bash
pyinstaller --onefile --windowed --icon=assets/icon.icns --name GW-Blocker src/main.py
```

### Linux
```bash
pyinstaller --onefile --name GW-Blocker src/main.py
```

The executable will be created in the `dist/` directory.

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a Pull Request.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/HarshYadav152/GW-blocker/issues/new?template=bug_report.md)
- 💡 **Feature Requests**: [Open an issue](https://github.com/HarshYadav152/GW-blocker/issues/new?template=feature_request.md)
- 📖 **Documentation**: Check the [Wiki](https://github.com/HarshYadav152/GW-blocker/wiki) (if available)

## Acknowledgments

- Built with Python and Tkinter
- Inspired by the need for digital wellness and productivity

## Roadmap

- [ ] Add whitelist functionality
- [ ] Implement scheduling (e.g., block during work hours)
- [ ] Add statistics and usage tracking
- [ ] Browser extension integration
- [ ] Mobile app version

---

**Star ⭐ this repository if you find it helpful!**