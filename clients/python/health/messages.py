from typing import Literal

from pydantic import BaseModel

from ..shared.messages import PingMessage, PongMessage

IncomingMessage = PongMessage
OutgoingMessage = PingMessage
