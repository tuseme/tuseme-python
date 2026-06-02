import pytest
import responses

from tuseme_sdk.exceptions import (
    AuthenticationError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from tuseme_sdk.http_client import HttpClient

BASE = "https://api.tuseme.co.ke/api/v1"


@pytest.fixture
def http():
    return HttpClient(
        api_key="tk_test_key",
        api_secret="sk_test_secret",
        max_retries=1,
    )


def _mock_auth():
    responses.add(
        responses.POST,
        f"{BASE}/auth/login",
        json={"access_token": "tok_abc", "expires_in": 3600},
        status=200,
    )


@responses.activate
def test_request_authenticates_and_returns_json(http):
    _mock_auth()
    responses.add(
        responses.GET,
        f"{BASE}/messages/msg_1",
        json={"data": {"message_id": "msg_1", "status": "delivered"}},
        status=200,
    )

    body = http.request("GET", "/messages/msg_1")

    assert body["data"]["message_id"] == "msg_1"
    assert len(responses.calls) == 2
    assert responses.calls[1].request.headers["Authorization"] == "Bearer tok_abc"


@responses.activate
def test_authentication_error_on_invalid_credentials(http):
    responses.add(
        responses.POST,
        f"{BASE}/auth/login",
        json={"detail": "Invalid credentials"},
        status=401,
    )

    with pytest.raises(AuthenticationError):
        http.request("GET", "/messages")


@responses.activate
def test_validation_error(http):
    _mock_auth()
    responses.add(
        responses.POST,
        f"{BASE}/messages/send",
        json={"detail": "Invalid sender_id"},
        status=400,
    )

    with pytest.raises(ValidationError):
        http.request("POST", "/messages/send", json={"content": "hi"})


@responses.activate
def test_rate_limit_error(http):
    _mock_auth()
    responses.add(
        responses.GET,
        f"{BASE}/messages",
        json={"detail": "Too many requests"},
        status=429,
        headers={"Retry-After": "10"},
    )

    with pytest.raises(RateLimitError) as exc_info:
        http.request("GET", "/messages")

    assert exc_info.value.retry_after == 10


@responses.activate
def test_server_error(http):
    _mock_auth()
    responses.add(
        responses.GET,
        f"{BASE}/messages",
        json={"detail": "Internal error"},
        status=500,
    )

    with pytest.raises(ServerError):
        http.request("GET", "/messages")
