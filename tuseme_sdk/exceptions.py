"""Exception classes for the Tuseme SDK."""


class TusemeError(Exception):
    """Base exception for all Tuseme SDK errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response or {}


class AuthenticationError(TusemeError):
    """Raised when authentication fails (invalid credentials or expired token)."""
    pass


class ValidationError(TusemeError):
    """Raised when the API rejects the request due to invalid parameters."""
    pass


class RateLimitError(TusemeError):
    """Raised when the API rate limit is exceeded."""

    def __init__(self, message: str, retry_after: int = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class ServerError(TusemeError):
    """Raised when the API returns a 5xx error."""
    pass


class NetworkError(TusemeError):
    """Raised when a network-level error occurs (timeout, DNS, etc.)."""
    pass
