from typing import Literal

from pydantic import BaseModel

from ..shared.messages import PingMessage, PongMessage


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
