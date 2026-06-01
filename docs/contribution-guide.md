# Contribution Guide

First off, thank you for considering contributing to GW-Blocker! It's people like you that make open source such a great community.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork locally**:
   ```bash
   git clone https://github.com/YourUsername/GW-blocker.git
   cd GW-blocker
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/my-awesome-feature
   ```

## Development Workflow

### Issue and Branch Workflow

- Open a clear issue before starting work whenever possible.
- Wait for a maintainer to review, approve, or assign the issue before implementing it.
- Create a dedicated branch for each change:
  - `feature/...` for new functionality
  - `fix/...` for bug fixes
  - `docs/...` for documentation updates
  - `ci/...` for workflow or automation improvements
- Keep each branch and PR focused on a single problem.

### Running the App

To test your changes, you will need to run the application with elevated privileges:

**Windows**:
```bash
# Run command prompt as Administrator
python -m src.main
```

**macOS/Linux**:
```bash
sudo python3 -m src.main
```

### Code Style Guidelines

- **PEP 8**: Ensure your Python code follows the PEP 8 style guide.
- **Docstrings**: Add docstrings to all new classes and methods explaining what they do.
- **Type Hinting**: Use Python type hints (e.g., `def clean_url(url: str) -> str:`) to make the codebase easier to understand.
- **Modularity**: Keep the GUI code separate from the system interaction logic.

## Submitting a Pull Request

1. **Commit your changes**:
   Make your commit messages clear and descriptive.
   ```bash
   git commit -m "Add feature: temporary block timers"
   ```
2. **Push to your fork**:
   ```bash
   git push origin feature/my-awesome-feature
   ```
3. **Open a Pull Request**:
   Go to the original repository on GitHub and open a pull request. Include a description of what you changed, why you changed it, and how to test it.

## Reporting Bugs

When opening an issue to report a bug, please include:
- A clear description of the problem.
- Steps to reproduce the issue.
- Your operating system and Python version.
- Screenshots if applicable.
