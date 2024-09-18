from datetime import date
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.travels import Travel, TravelList, TravelPublic
from zupit.service.travels_crud import (
    confirm_travel_db,
    create_travel_db,
    get_travel_by_user,
    get_travel_db,
    search_travel_db,
)
from zupit.utils import get_current_user

router = APIRouter(prefix='/travels', tags=['travels'])

templates = Jinja2Templates(directory='zupit/templates')
Session = Annotated[Session, Depends(get_session)]


@router.post(
    '/',
    response_class=HTMLResponse,
    status_code=HTTPStatus.CREATED,
)
def crate_travel(
    request: Request,
    session: Session,  # type: ignore
    travel: Travel,
):
    try:
        create_travel_db(session, travel)
        return RedirectResponse(
            url='/profile/', status_code=HTTPStatus.SEE_OTHER
        )
    except HTTPException as exc:
        request.session['error'] = exc.detail
        return RedirectResponse(
            url='/offer/fifth', status_code=HTTPStatus.SEE_OTHER
        )


@router.get('/{user_id}/', response_model=TravelList)
def get_travel(
    session: Session,  # type: ignore
    user_id: int,
):
    if travel_list := get_travel_by_user(session, user_id):
        return travel_list
    return None


@router.get('/search/{travel_id}/', response_model=TravelPublic)
def get_travel_by_id(
    session: Session,  # type: ignore
    travel_id: int,
):
    if specific_travel := get_travel_db(session, travel_id):
        return specific_travel
    return None


@router.post('/search-travels/', response_class=HTMLResponse)
def search_travels(
    request: Request,
    session: Session,  # type: ignore
    leaving: Annotated[str, Form()],
    going: Annotated[str, Form()],
    day: Annotated[date, Form()],
):
    try:
        travel_list = search_travel_db(session, leaving, going, day)
        return templates.TemplateResponse(
            'result-search-travel.html',
            {'request': request, 'travels': travel_list.travels},
        )
    except HTTPException as exc:
        request.session['error'] = exc.detail
        return RedirectResponse(
            url='/search-travel', status_code=HTTPStatus.SEE_OTHER
        )


@router.get('/confirm_travel/{travel_id}', response_class=HTMLResponse)
def confirm_travel(
    request: Request,
    session: Session,  # type: ignore
    travel_id: int,
):
    try:
        if user := get_current_user(request, session):
            confirm_travel_db(session, user.id, travel_id)

            return templates.TemplateResponse(
                request=request,
                name='profile/my-travels.html',
                context={'user': user},
            )
        request.session['error'] = 'Você precisa estar logado'
        return RedirectResponse(
            url='/sign-in', status_code=HTTPStatus.SEE_OTHER
        )
    except HTTPException as exc:
        request.session['error'] = exc.detail
        return RedirectResponse(
            url='/search-travel', status_code=HTTPStatus.SEE_OTHER
        )
