# Contributing to GW-Blocker

Thank you for your interest in contributing to GW-Blocker! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details** (OS, Python version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** for the enhancement
- **Possible implementation** approach (optional)

### Pull Requests

1. Fork the repository
2. Create an issue describing the change before implementing it
3. Create a dedicated branch for your work:
   - `feature/...` for enhancements
   - `fix/...` for bug fixes
   - `docs/...` for documentation updates
   - `ci/...` for workflow or automation changes
4. Make your changes in a focused branch
5. Test your changes thoroughly
6. Commit your changes with a clear message
7. Push to the branch (`git push origin feature/your-feature-name`)
8. Open a Pull Request and link the related issue

#### Pull Request Guidelines

- Follow the existing code style
- Add comments for complex logic
- Update documentation if needed
- Test on multiple platforms if possible
- Keep commits focused and atomic
- Keep unrelated changes out of the same PR
- Include a short summary and testing steps in the PR description

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/HarshYadav152/GW-blocker.git
cd GW-blocker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
# Windows (as administrator)
python -m src.main

# macOS/Linux
sudo python3 -m src.main
```

## Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

## Testing

Before submitting a pull request:

- Test the application on your platform
- Verify that blocking and unblocking works correctly
- Check that the timer functionality works as expected
- Ensure no errors in the console

## Documentation

- Update the [README.md](README.md) if you change functionality
- Add comments for complex code sections
- Update installation instructions if dependencies change

## Questions?

Feel free to open an issue for any questions about contributing!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.