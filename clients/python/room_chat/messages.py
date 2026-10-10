from typing import Literal

from pydantic import BaseModel


class PingMessage(BaseModel):
    """Simple ping message to check WebSocket connection status."""

    action: Literal["ping"] = "ping"
    payload: None = None


class PongMessage(BaseModel):
    """Simple pong message response to ping requests."""

    action: Literal["pong"] = "pong"
    payload: None = None


class RoomMessagePayload(BaseModel):
    """RoomMessagePayload"""

    message: str
    room_name: str | None = None


class RoomChatMessage(BaseModel):
    """A chat message a client sends to its room."""

    action: Literal["room_chat"] = "room_chat"
    payload: RoomMessagePayload


class RoomNotificationMessage(BaseModel):
    """A chat message broadcast to everyone in the room."""

    action: Literal["room_notification"] = "room_notification"
    payload: RoomMessagePayload


IncomingMessage = PongMessage | RoomNotificationMessage
OutgoingMessage = PingMessage | RoomChatMessage
