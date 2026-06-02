"""Top-level Tuseme API client."""

from tuseme_sdk.http_client import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, MAX_RETRIES, HttpClient
from tuseme_sdk.messages import Messages


class TusemeClient:
    """
    Official Tuseme SMS API client.

    Usage::

        from tuseme import TusemeClient

        client = TusemeClient(
            api_key="tk_test_...",
            api_secret="sk_test_...",
        )

        # Send SMS
        response = client.messages.send(
            content="Hello!",
            sender_id="TUSEME-LTD",
            recipients=[{"msisdn": "+254712345678"}],
        )

    Args:
        api_key: Your Tuseme API Key (starts with tk_test_ or tk_live_).
        api_secret: Your Tuseme API Secret (starts with sk_test_ or sk_live_).
        base_url: API base URL (default: https://api.tuseme.co.ke/api/v1).
        timeout: Request timeout in seconds (default: 30).
        max_retries: Maximum number of retry attempts (default: 3).
    """

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES,
    ):
        if not api_key:
            raise ValueError("api_key is required")
        if not api_secret:
            raise ValueError("api_secret is required")

        self._http = HttpClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

        self.messages = Messages(self._http)

    @property
    def is_sandbox(self) -> bool:
        """Whether this client is using sandbox credentials."""
        return self._http.api_key.startswith("tk_test_")

    @property
    def is_production(self) -> bool:
        """Whether this client is using production credentials."""
        return self._http.api_key.startswith("tk_live_")
