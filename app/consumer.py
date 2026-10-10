from chanx.core.decorators import channel, ws_handler
from chanx.fast_channels.websocket import AsyncJsonWebsocketConsumer
from chanx.messages.incoming import PingMessage
from chanx.messages.outgoing import PongMessage

from .messages import RoomChatMessage, RoomMessagePayload, RoomNotificationMessage


@channel(name="room_chat", description="Chat with everyone in one room", tags=["chat"])
class RoomChatConsumer(AsyncJsonWebsocketConsumer):
    channel_layer_alias = "chat"

    @ws_handler(summary="Check the connection")
    async def handle_ping(self, _message: PingMessage) -> PongMessage:
        return PongMessage()

    @ws_handler(
        summary="Send a message to the room",
        output_type=RoomNotificationMessage,
    )
    async def handle_room_chat(self, message: RoomChatMessage) -> None:
        await self.broadcast_message(
            RoomNotificationMessage(
                payload=RoomMessagePayload(
                    message=message.payload.message,
                    room_name=self.room_name,
                )
            ),
            groups=[self.room_group],
        )

    async def post_authentication(self) -> None:
        self.room_name: str = self.scope["path_params"]["room_name"]
        self.room_group = f"room_{self.room_name}"
        await self.channel_layer.group_add(self.room_group, self.channel_name)
        self.groups.append(self.room_group)
