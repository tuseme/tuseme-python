"""Messages API resource."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from tuseme_sdk.http_client import HttpClient


@dataclass
class SendResponse:
    """Response from sending a message."""
    success: bool
    message_id: str = ""
    batch_id: str = ""
    status: str = ""
    message: str = ""
    estimated_cost: Optional[float] = None
    currency: str = "KES"
    selected_provider: Optional[str] = None
    recipient_count: int = 0
    timestamp: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MessageStatus:
    """Response from getting message status."""
    message_id: str = ""
    status: str = ""
    recipient: str = ""
    sender_id: str = ""
    content: str = ""
    provider: Optional[str] = None
    cost: Optional[float] = None
    currency: str = "KES"
    created_at: str = ""
    delivered_at: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


class Messages:
    """
    Messages API.

    Usage::

        response = client.messages.send(
            content="Hello!",
            sender_id="TUSEME-LTD",
            recipients=[{"msisdn": "+254712345678"}],
        )
    """

    def __init__(self, http: HttpClient):
        self._http = http

    def send(
        self,
        content: str,
        recipients: List[Dict[str, str]],
        sender_id: str = "TUSEME-LTD",
        type: str = "promotional",
        priority: str = "MEDIUM",
        scheduled_for: Optional[str] = None,
        timezone: str = "Africa/Nairobi",
        metadata: Optional[Dict[str, Any]] = None,
        group_ids: Optional[List[str]] = None,
        contact_ids: Optional[List[str]] = None,
    ) -> SendResponse:
        """
        Send an SMS to one or more recipients.

        Args:
            content: Message body (1–918 characters).
            recipients: List of dicts with 'msisdn' (required) and 'name' (optional).
            sender_id: Registered alphanumeric sender ID (max 11 chars).
            type: "transactional" or "promotional".
            priority: "HIGH", "MEDIUM", or "LOW".
            scheduled_for: ISO 8601 datetime for scheduled delivery.
            timezone: IANA timezone (default: Africa/Nairobi).
            metadata: Custom key-value pairs.
            group_ids: IDs of pre-defined contact groups.
            contact_ids: IDs of individual contacts.

        Returns:
            SendResponse with message_id, batch_id, status, etc.

        Raises:
            ValidationError: If the request parameters are invalid.
            AuthenticationError: If credentials are invalid or expired.
        """
        payload: Dict[str, Any] = {
            "content": content,
            "sender_id": sender_id,
            "type": type,
            "priority": priority,
        }

        if recipients:
            payload["recipients"] = recipients
        if group_ids:
            payload["group_ids"] = group_ids
        if contact_ids:
            payload["contact_ids"] = contact_ids
        if scheduled_for:
            payload["scheduled_for"] = scheduled_for
            payload["timezone"] = timezone
        if metadata:
            payload["metadata"] = metadata

        data = self._http.request("POST", "/messages/send", json=payload)

        return SendResponse(
            success=data.get("success", True),
            message_id=data.get("message_id", ""),
            batch_id=data.get("batch_id", ""),
            status=data.get("status", ""),
            message=data.get("message", ""),
            estimated_cost=data.get("estimated_cost"),
            currency=data.get("currency", "KES"),
            selected_provider=data.get("selected_provider"),
            recipient_count=data.get("recipient_count", 0),
            timestamp=data.get("timestamp", ""),
            raw=data,
        )

    def get(self, message_id: str) -> MessageStatus:
        """
        Get the delivery status of a message.

        Args:
            message_id: The ID returned from send().

        Returns:
            MessageStatus with current delivery information.
        """
        data = self._http.request("GET", f"/messages/{message_id}")
        info = data.get("data", data)

        return MessageStatus(
            message_id=info.get("message_id", message_id),
            status=info.get("status", ""),
            recipient=info.get("recipient", ""),
            sender_id=info.get("sender_id", ""),
            content=info.get("content", ""),
            provider=info.get("provider"),
            cost=info.get("cost"),
            currency=info.get("currency", "KES"),
            created_at=info.get("created_at", ""),
            delivered_at=info.get("delivered_at"),
            raw=data,
        )

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        List sent messages with pagination and filtering.

        Args:
            page: Page number (default 1).
            page_size: Number of results per page (default 20, max 100).
            status: Filter by status (e.g. "delivered", "failed").
            date_from: ISO 8601 date to filter from.
            date_to: ISO 8601 date to filter to.

        Returns:
            Dict with 'data' (list of messages), 'total', 'page', 'page_size'.
        """
        params: Dict[str, Any] = {
            "page": page,
            "page_size": page_size,
        }
        if status:
            params["status"] = status
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to

        return self._http.request("GET", "/messages", params=params)
