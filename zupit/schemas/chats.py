from datetime import datetime

from pydantic import BaseModel


class Chat(BaseModel):
    id: int
    first: str
    second: str


class ChatList(BaseModel):
    chats: list[Chat]


class Message(BaseModel):
    sender: str
    message: str
    created_at: datetime


class MessageList(BaseModel):
    messages: list[Message]
