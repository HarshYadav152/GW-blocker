# Deployment & Building from Source

GW-Blocker can be compiled into a standalone executable that doesn't require users to have Python installed on their machines. We use `PyInstaller` for this process.

## Prerequisites

Before building the application, ensure you have PyInstaller installed:

```bash
pip install pyinstaller
```

## Building for Windows

To build a standalone `.exe` on Windows that will request Administrator privileges upon execution:

```bash
pyinstaller --onefile --windowed --uac-admin --icon=assets/icon.ico --name GW-Blocker src/main.py
```

- `--onefile`: Bundles everything into a single `.exe`.
- `--windowed`: Hides the console window so only the GUI appears.
- `--uac-admin`: Prompts the user for Administrator privileges automatically.

## Building for macOS

To build a standalone `.app` for macOS:

```bash
pyinstaller --onefile --windowed --icon=assets/icon.icns --name GW-Blocker src/main.py
```

*Note: On macOS, elevated privileges cannot be easily baked into the app bundle in the same way as Windows UAC. Users may need to launch the app securely or the app will prompt for a password when modifying `/etc/hosts`.*

## Building for Linux

To build a standalone binary for Linux:

```bash
pyinstaller --onefile --name GW-Blocker src/main.py
```

## Output

After running the build command, the executable will be located in the automatically generated `dist/` directory. You can distribute this file directly to end-users.
