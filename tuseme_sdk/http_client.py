"""Low-level HTTP transport with authentication and retry logic."""

import time
import logging
from typing import Any, Dict, Optional

import requests

from tuseme_sdk.exceptions import (
    AuthenticationError,
    NetworkError,
    RateLimitError,
    ServerError,
    TusemeError,
    ValidationError,
)

logger = logging.getLogger("tuseme")

DEFAULT_BASE_URL = "https://api.tuseme.co.ke/api/v1"
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_BACKOFF = 0.5  # seconds


class HttpClient:
    """Handles HTTP requests, auth token lifecycle, and retries."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES,
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

        self._session = requests.Session()
        self._session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "tuseme-python/1.0.0",
        })

        # Token state
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0

    # ── Authentication ───────────────────────────────────────

    def _authenticate(self) -> None:
        """Obtain a fresh access token from the auth endpoint."""
        try:
            resp = self._session.post(
                f"{self.base_url}/auth/login",
                json={
                    "api_key": self.api_key,
                    "api_secret": self.api_secret,
                },
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise NetworkError(f"Authentication request failed: {exc}") from exc

        if resp.status_code == 401:
            raise AuthenticationError(
                "Invalid API credentials. Check your api_key and api_secret.",
                status_code=401,
                response=resp.json() if resp.content else {},
            )

        if resp.status_code != 200:
            raise AuthenticationError(
                f"Authentication failed with status {resp.status_code}",
                status_code=resp.status_code,
            )

        data = resp.json()
        self._access_token = data["access_token"]
        # Expire 60 s early to avoid edge-case expiry mid-request
        self._token_expires_at = time.time() + data.get("expires_in", 3600) - 60
        logger.debug("Authenticated successfully (expires_in=%s)", data.get("expires_in"))

    def _ensure_auth(self) -> None:
        """Authenticate if we don't have a valid token."""
        if not self._access_token or time.time() >= self._token_expires_at:
            self._authenticate()
        self._session.headers["Authorization"] = f"Bearer {self._access_token}"

    # ── Request execution ────────────────────────────────────

    def request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute an API request with automatic auth, retry, and error handling."""
        self._ensure_auth()
        url = f"{self.base_url}{path}"

        last_exc: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = self._session.request(
                    method=method,
                    url=url,
                    json=json,
                    params=params,
                    timeout=self.timeout,
                )
                return self._handle_response(resp)

            except (RateLimitError, ServerError, NetworkError) as exc:
                last_exc = exc
                if attempt < self.max_retries:
                    wait = RETRY_BACKOFF * (2 ** (attempt - 1))
                    if isinstance(exc, RateLimitError) and exc.retry_after:
                        wait = exc.retry_after
                    logger.warning(
                        "Request to %s failed (attempt %d/%d), retrying in %.1fs: %s",
                        path, attempt, self.max_retries, wait, exc,
                    )
                    time.sleep(wait)

            except AuthenticationError:
                # Token may have expired mid-flight; re-auth once
                if attempt == 1:
                    self._access_token = None
                    self._ensure_auth()
                else:
                    raise

        raise last_exc  # type: ignore[misc]

    # ── Response handling ────────────────────────────────────

    @staticmethod
    def _handle_response(resp: requests.Response) -> Dict[str, Any]:
        """Parse response and raise appropriate exceptions."""
        try:
            body = resp.json() if resp.content else {}
        except ValueError:
            body = {"raw": resp.text}

        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 5))
            raise RateLimitError(
                "Rate limit exceeded",
                retry_after=retry_after,
                status_code=429,
                response=body,
            )

        if resp.status_code == 401:
            raise AuthenticationError(
                body.get("detail", "Authentication failed"),
                status_code=401,
                response=body,
            )

        if resp.status_code == 400:
            detail = body.get("detail", body)
            raise ValidationError(
                f"Validation error: {detail}",
                status_code=400,
                response=body,
            )

        if resp.status_code >= 500:
            raise ServerError(
                f"Server error: {resp.status_code}",
                status_code=resp.status_code,
                response=body,
            )

        if resp.status_code >= 400:
            raise TusemeError(
                f"API error: {resp.status_code}",
                status_code=resp.status_code,
                response=body,
            )

        return body
