"""
Tuseme SDK — Official Python client for the Tuseme SMS API.

Usage::

    from tuseme import TusemeClient

    client = TusemeClient(
        api_key="tk_test_...",
        api_secret="sk_test_...",
    )

    response = client.messages.send(
        content="Hello from Tuseme!",
        sender_id="TUSEME-LTD",
        recipients=[{"msisdn": "+254712345678"}],
    )
    print(response.message_id)
"""

__version__ = "1.0.0"

from tuseme_sdk.client import TusemeClient  # noqa: F401
from tuseme_sdk.exceptions import (  # noqa: F401
    TusemeError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    ServerError,
)

__all__ = [
    "TusemeClient",
    "TusemeError",
    "AuthenticationError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
]
