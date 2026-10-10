from typing import Literal

from chanx.messages.base import BaseMessage
from pydantic import BaseModel


class RoomMessagePayload(BaseModel):
    message: str
    room_name: str | None = None


class RoomChatMessage(BaseMessage):
    """A chat message a client sends to its room."""

    action: Literal["room_chat"] = "room_chat"
    payload: RoomMessagePayload


class RoomNotificationMessage(BaseMessage):
    """A chat message broadcast to everyone in the room."""

    action: Literal["room_notification"] = "room_notification"
    payload: RoomMessagePayload
