import { createClient } from '@chanx-js/client';

import { roomChat } from './generated';

const client = createClient({ baseUrl: 'ws://localhost:8000' });

// `room_name` is required: the channel address in the spec is /ws/room/{room_name}.
const conn = client.connect(roomChat, { params: { room_name: 'lobby' } });

conn.on('room_notification', (msg) => {
  // Narrowed by `action`, so the payload type is known here.
  show(msg.payload.message);
});

export function send(text: string) {
  conn.send({ action: 'room_chat', payload: { message: text } });
}

function show(text: string) {
  const li = document.createElement('li');
  li.textContent = text;
  document.querySelector('#messages')?.append(li);
}
