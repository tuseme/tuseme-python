# Changelog

All notable changes to the Tuseme Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-25

### Added
- Initial release of the Tuseme Python SDK.
- `TusemeClient` with automatic authentication and token refresh.
- `messages.send()` — send SMS to one or more recipients.
- `messages.get()` — check delivery status of a message.
- `messages.list()` — list sent messages with pagination and filtering.
- Built-in retry logic with exponential backoff.
- Typed exception hierarchy: `AuthenticationError`, `ValidationError`, `RateLimitError`, `ServerError`, `NetworkError`.
- Sandbox and production credential detection.
