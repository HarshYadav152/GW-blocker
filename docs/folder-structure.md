# Folder Structure

Understanding the project's folder structure is crucial for navigating the codebase and contributing effectively.

```text
GW-blocker/
├── .github/                # GitHub Actions workflows and issue templates
├── src/                    # Source code directory
│   ├── __init__.py         # Marks the directory as a Python package
│   ├── main.py             # Entry point of the application
│   ├── gui.py              # Tkinter graphical user interface implementation
│   ├── blocker.py          # Core logic for modifying the hosts file
│   └── utils.py            # Helper functions for URL parsing and config management
├── docs/                   # Documentation files (you are here)
│   ├── installation.md     # Installation guide
│   ├── architecture.md     # Architecture overview
│   ├── contribution-guide.md # Guidelines for contributing
│   ├── deployment.md       # Build & deployment instructions
│   ├── api.md              # Internal API documentation
│   └── folder-structure.md # Details about project directory (this file)
├── assets/                 # Icons and static resources for the application
├── dist/                   # (Generated) Compiled executables created by PyInstaller
├── build/                  # (Generated) Temporary build files created by PyInstaller
├── CODE_OF_CONDUCT.md      # Rules for community interaction
├── CONTRIBUTING.md         # Quick reference for contributing to the repository
├── LICENSE                 # MIT License details
├── README.md               # Main project overview and introduction
└── requirements.txt        # Python dependencies
```

## Key Directories

- **`src/`**: Contains the main application logic. All functional code is kept here to maintain a clean root directory.
- **`docs/`**: Holds all the extended documentation (architecture, deployment, APIs, etc.) to keep the main `README.md` concise.
- **`assets/`**: Put any icons (`.ico`, `.icns`), images, or branding materials here. These are used during the PyInstaller build process.
