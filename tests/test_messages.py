import responses

from tuseme_sdk.client import TusemeClient

BASE = "https://api.tuseme.co.ke/api/v1"


def _mock_auth():
    responses.add(
        responses.POST,
        f"{BASE}/auth/login",
        json={"access_token": "tok_abc", "expires_in": 3600},
        status=200,
    )


@responses.activate
def test_send_message():
    _mock_auth()
    responses.add(
        responses.POST,
        f"{BASE}/messages/send",
        json={
            "success": True,
            "message_id": "msg_123",
            "batch_id": "batch_456",
            "status": "queued",
            "recipient_count": 1,
        },
        status=200,
    )

    client = TusemeClient(api_key="tk_test_key", api_secret="sk_test_secret")
    result = client.messages.send(
        content="Hello!",
        sender_id="TUSEME-LTD",
        recipients=[{"msisdn": "+254712345678"}],
    )

    assert result.success is True
    assert result.message_id == "msg_123"
    assert result.batch_id == "batch_456"
    assert result.status == "queued"
    assert result.recipient_count == 1


@responses.activate
def test_get_message_status():
    _mock_auth()
    responses.add(
        responses.GET,
        f"{BASE}/messages/msg_123",
        json={
            "data": {
                "message_id": "msg_123",
                "status": "delivered",
                "recipient": "+254712345678",
            }
        },
        status=200,
    )

    client = TusemeClient(api_key="tk_test_key", api_secret="sk_test_secret")
    status = client.messages.get("msg_123")

    assert status.message_id == "msg_123"
    assert status.status == "delivered"
    assert status.recipient == "+254712345678"
