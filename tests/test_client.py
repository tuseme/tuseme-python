import pytest

from tuseme_sdk import TusemeClient


def test_client_requires_api_key():
    with pytest.raises(ValueError, match="api_key"):
        TusemeClient(api_key="", api_secret="sk_test_secret")


def test_client_requires_api_secret():
    with pytest.raises(ValueError, match="api_secret"):
        TusemeClient(api_key="tk_test_key", api_secret="")


def test_sandbox_credentials():
    client = TusemeClient(api_key="tk_test_key", api_secret="sk_test_secret")
    assert client.is_sandbox is True
    assert client.is_production is False


def test_production_credentials():
    client = TusemeClient(api_key="tk_live_key", api_secret="sk_live_secret")
    assert client.is_sandbox is False
    assert client.is_production is True
