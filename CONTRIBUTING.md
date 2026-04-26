# Contributing to Tuseme Python SDK

Thank you for your interest in contributing! Here's how to get started.

## Development Setup

```bash
git clone https://github.com/tuseme/tuseme-python.git
cd tuseme-python
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest --cov=tuseme_sdk tests/
```

## Code Style

We use **Black** for formatting and **Ruff** for linting:

```bash
black tuseme_sdk/
ruff check tuseme_sdk/
```

## Pull Requests

1. Fork the repo and create a feature branch from `main`.
2. Add tests for any new functionality.
3. Ensure all tests pass and linting is clean.
4. Open a PR with a clear description of the change.

## Reporting Issues

Open an issue at [github.com/tuseme/tuseme-python/issues](https://github.com/tuseme/tuseme-python/issues) with:
- SDK version and Python version
- Minimal reproduction steps
- Expected vs. actual behavior
