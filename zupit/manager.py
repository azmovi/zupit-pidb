from http import HTTPStatus
from typing import Self

from fastapi import HTTPException, WebSocket
from sqlalchemy import text

from zupit.database import get_session


class ConnectionManager:
    def __init__(self) -> None:
        self.connections: dict[int, list[WebSocket]] = {}

    async def connect(self: Self, websocket: WebSocket, chat_id: int):
        await websocket.accept()
        if chat_id not in self.connections:
            self.connections[chat_id] = []
        self.connections[chat_id].append(websocket)

    async def disconnect(self: Self, websocket: WebSocket, chat_id: int):
        self.connections[chat_id].remove(websocket)
        if not self.connections[chat_id]:
            del self.connections[chat_id]

    @staticmethod
    async def send_message(message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self: Self, message: str, chat_id: int):
        if chat_id in self.connections:
            for connection in self.connections[chat_id]:
                await connection.send_text(message)

        await save_message(chat_id, message)


async def save_message(chat_id: int, message: str):
    sender_id, content = message.split('-', 1)

    sql = text('SELECT * FROM save_message(:chat_id, :sender_id, :content)')
    session = next(get_session())
    try:
        session.execute(
            sql,
            {
                'chat_id': chat_id,
                'sender_id': sender_id,
                'content': content,
            },
        )
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Invalid Input'
        )


manager = ConnectionManager()
