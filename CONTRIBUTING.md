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

## Branch Protection & Pull Requests

The `main` branch is protected with the following rules:

- **Pull requests are required** — direct pushes to `main` are blocked.
- **1 approving review** is needed before merging.
- **CI status checks** (`lint` and `test`) must pass.
- **Branches must be up to date** with `main` before merging.
- **Linear history** is enforced (squash or rebase merges only).
- **Stale approvals are dismissed** when new commits are pushed.

### How to Submit a PR

1. **Fork** the repo and clone your fork.
2. Create a **feature branch** from `main`:
   ```bash
   git checkout -b feature/my-improvement
   ```
3. Make your changes and **add tests** for any new functionality.
4. Ensure all tests pass and linting is clean:
   ```bash
   black tuseme_sdk/ && ruff check tuseme_sdk/
   pytest --cov=tuseme_sdk tests/
   ```
5. Commit with a descriptive message following [Conventional Commits](https://www.conventionalcommits.org/):
   ```bash
   git commit -m "feat: add batch message scheduling"
   ```
6. Push your branch and **open a PR** against `main`:
   ```bash
   git push origin feature/my-improvement
   gh pr create --title "feat: add batch message scheduling" --body "Description..."
   ```
7. Wait for CI to pass and a maintainer to review.

## Release Process

Releases are handled by maintainers. The process is:

1. Update the version in `pyproject.toml` (`version = "X.Y.Z"`).
2. Update `CHANGELOG.md` with the new version section.
3. Commit: `git commit -m "chore: bump version to vX.Y.Z"`
4. Tag: `git tag -a vX.Y.Z -m "vX.Y.Z — Description"`
5. Push: `git push origin main && git push origin vX.Y.Z`
6. CI automatically publishes to **PyPI** via Trusted Publisher (OIDC).
7. Create a GitHub Release: `gh release create vX.Y.Z --repo tuseme/tuseme-python`

We follow [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`).

## Reporting Issues

Open an issue at [github.com/tuseme/tuseme-python/issues](https://github.com/tuseme/tuseme-python/issues) with:
- SDK version and Python version
- Minimal reproduction steps
- Expected vs. actual behavior
