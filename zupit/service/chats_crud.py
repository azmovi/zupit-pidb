from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.chats import Chat, ChatList, Message, MessageList

Session = Annotated[Session, Depends(get_session)]


def create_chat_db(
    session: Session,  # type: ignore
    first: int,
    second: int,
):
    sql = text('SELECT * FROM create_chat(:first, :second)')
    try:
        session.execute(sql, {'first': first, 'second': second})
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Invalid chat creation'
        )


def get_chats_db(
    session: Session,  # type: ignore
    user_id: int,
) -> ChatList:
    chat_list = []
    sql = text('SELECT * FROM get_chats(:user_id)')
    chats = session.execute(sql, {'user_id': user_id}).fetchall()
    for chat in chats:
        chat_example = Chat(
            id=chat[0],
            first=chat[1],
            second=chat[2],
        )
        chat_list.append(chat_example)

    return ChatList(chats=chat_list)


def get_chat_db(
    session: Session,  # type:  ignore
    first: int,
    second: int,
) -> Optional[int]:
    sql = text('SELECT * FROM get_chat(:first, :second)')
    try:
        result = session.execute(
            sql, {'first': first, 'second': second}
        ).fetchone()
        session.commit()
        if result:
            return result[0]
        return None
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Invalid Input'
        )


def get_messages_db(
    session: Session,  # type: ignore
    chat_id: int,
) -> MessageList:
    message_list = []
    sql = text('SELECT * FROM get_messages(:chat_id)')
    messages = session.execute(sql, {'chat_id': chat_id}).fetchall()
    for message in messages:
        message_example = Message(
            sender=message[0],
            message=message[1],
            created_at=message[2],
        )
        message_list.append(message_example)

    return MessageList(messages=message_list)


def get_users_from_chat_db(
    session: Session,  # type: ignore
    chat_id: int,
    user_id: int,
) -> Chat:
    sql = text('SELECT * FROM get_users_from_chat(:chat_id, :user_id)')
    try:
        result = session.execute(
            sql, {'chat_id': chat_id, 'user_id': user_id}
        ).fetchone()
        session.commit()
        return Chat(id=chat_id, first=result[0], second=result[1])
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Invalid Input'
        )
