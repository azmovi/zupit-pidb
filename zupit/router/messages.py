from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.manager import manager
from zupit.service.chats_crud import get_messages_db, get_users_from_chat_db
from zupit.utils import get_current_user

router = APIRouter(prefix='/messages', tags=['messages'])
templates = Jinja2Templates(directory='zupit/templates')
Session = Annotated[Session, Depends(get_session)]


@router.get('/{chat_id}/', response_class=HTMLResponse)
def get_messages(
    request: Request,
    session: Session,  # type: ignore
    chat_id: int,
):
    if user := get_current_user(request, session):
        chat = get_users_from_chat_db(session, chat_id, user.id)
        messages = get_messages_db(session, chat_id)
        return templates.TemplateResponse(
            request=request,
            name='messages.html',
            context={
                'user': user,
                'chat': chat,
                'messages': messages.messages,
            },
        )
    return RedirectResponse(url='/sign-in', status_code=HTTPStatus.SEE_OTHER)


@router.websocket('/ws/{chat_id}/')
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    await manager.connect(websocket, chat_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, chat_id)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, chat_id)
