# Tuseme Python SDK

Official Python client for the [Tuseme SMS API](https://docs.tuseme.co.ke).

[![PyPI version](https://badge.fury.io/py/tuseme-sdk.svg)](https://pypi.org/project/tuseme-sdk/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Installation

```bash
pip install tuseme-sdk
```

## Quick Start

```python
from tuseme import TusemeClient

client = TusemeClient(
    api_key="tk_test_your_api_key",
    api_secret="sk_test_your_api_secret",
)

# Send an SMS
response = client.messages.send(
    content="Hello from Tuseme! Your OTP is 482910.",
    sender_id="TUSEME-LTD",
    recipients=[
        {"msisdn": "+254712345678", "name": "John Doe"}
    ],
    type="transactional",
    priority="HIGH",
)

print(f"Message ID: {response.message_id}")
print(f"Status: {response.status}")
```

## Authentication

The SDK handles authentication automatically. Just provide your API Key and Secret (from the [Tuseme Dashboard](https://app.tuseme.co.ke)):

```python
# Sandbox credentials (for testing)
client = TusemeClient(api_key="tk_test_...", api_secret="sk_test_...")

# Production credentials
client = TusemeClient(api_key="tk_live_...", api_secret="sk_live_...")
```

The SDK will:
1. Automatically obtain an access token on the first request
2. Cache the token until it expires
3. Transparently refresh expired tokens

## Usage

### Send SMS

```python
# Single recipient
response = client.messages.send(
    content="Your verification code is 123456",
    sender_id="TUSEME-LTD",
    recipients=[{"msisdn": "+254712345678"}],
    type="transactional",
)

# Multiple recipients
response = client.messages.send(
    content="Flash sale! 50% off today only.",
    sender_id="TUSEME-LTD",
    recipients=[
        {"msisdn": "+254712345678", "name": "Alice"},
        {"msisdn": "+254798765432", "name": "Bob"},
    ],
    type="promotional",
    priority="MEDIUM",
)

# With metadata
response = client.messages.send(
    content="Your order #12345 has shipped!",
    sender_id="TUSEME-LTD",
    recipients=[{"msisdn": "+254712345678"}],
    metadata={"order_id": "12345", "campaign": "order_updates"},
)
```

### Check Delivery Status

```python
status = client.messages.get("msg_a1b2c3d4...")
print(f"Status: {status.status}")
print(f"Delivered at: {status.delivered_at}")
```

### List Messages

```python
result = client.messages.list(page=1, page_size=20, status="delivered")
for msg in result["data"]:
    print(f"{msg['recipient']}: {msg['status']}")
```

## Error Handling

```python
from tuseme import TusemeClient, AuthenticationError, ValidationError, RateLimitError

client = TusemeClient(api_key="...", api_secret="...")

try:
    response = client.messages.send(
        content="Hello!",
        recipients=[{"msisdn": "+254712345678"}],
    )
except AuthenticationError:
    print("Invalid credentials — check your API key and secret")
except ValidationError as e:
    print(f"Invalid request: {e}")
except RateLimitError as e:
    print(f"Rate limited — retry after {e.retry_after}s")
```

## Configuration

```python
client = TusemeClient(
    api_key="...",
    api_secret="...",
    base_url="https://api.tuseme.co.ke/api/v1",  # default
    timeout=30,       # request timeout in seconds
    max_retries=3,    # automatic retries on failure
)
```

## License

MIT — see [LICENSE](LICENSE).
