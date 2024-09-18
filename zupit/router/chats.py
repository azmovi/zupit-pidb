from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.service.chats_crud import create_chat_db, get_chat_db, get_chats_db

router = APIRouter(prefix='/chats', tags=['chats'])
templates = Jinja2Templates(directory='zupit/templates')
Session = Annotated[Session, Depends(get_session)]


@router.post(
    '/{first}/{second}',
    response_class=HTMLResponse,
    status_code=HTTPStatus.CREATED,
)
def create_chat(
    request: Request,
    session: Session,  # type: ignore
    first: int,
    second: int,
):
    try:
        if not get_chat_db(session, first, second):
            create_chat_db(session, first, second)

        return RedirectResponse(url='/chats', status_code=HTTPStatus.SEE_OTHER)

    except HTTPException as exc:
        request.session['error'] = exc.detail
        return RedirectResponse(
            url='/search-travel', status_code=HTTPStatus.SEE_OTHER
        )


@router.get('/{user_id}/', response_class=HTMLResponse)
def get_chats(
    session: Session,  # type: ignore
    user_id: int,
):
    return get_chats_db(session, user_id)


@router.get('/{first}/{second}', response_class=HTMLResponse)
def get_chat_by_users(
    request: Request,
    session: Session,  # type: ignore
    first: int,
    second: int,
):
    if first == second:
        return RedirectResponse(
            url=f'/trip-participants/{first}', status_code=HTTPStatus.SEE_OTHER
        )
    if chat_id := get_chat_db(session, first, second):
        return RedirectResponse(
            url=f'/messages/{chat_id}', status_code=HTTPStatus.SEE_OTHER
        )
    else:
        return create_chat(request, session, first, second)
