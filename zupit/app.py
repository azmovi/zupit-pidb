from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from .database import get_session
from .router import (
    cars,
    chats,
    drivers,
    messages,
    offer,
    profile,
    rate,
    travels,
    users,
)
from .utils import get_current_driver, get_current_user

app = FastAPI()

app.mount('/static', StaticFiles(directory='zupit/static'), name='static')
templates = Jinja2Templates(directory='zupit/templates')
app.add_middleware(SessionMiddleware, secret_key='secret_key')

app.include_router(users.router)
app.include_router(drivers.router)
app.include_router(cars.router)
app.include_router(offer.router)
app.include_router(travels.router)
app.include_router(rate.router)
app.include_router(profile.router)
app.include_router(chats.router)
app.include_router(messages.router)

Session = Annotated[Session, Depends(get_session)]


@app.get('/', response_class=HTMLResponse)
def reset_session():
    return RedirectResponse(url='/logoff', status_code=HTTPStatus.SEE_OTHER)


@app.get('/logoff', response_class=HTMLResponse)
def logoff(request: Request):
    request.session.clear()
    return RedirectResponse(
        url='/search-travel', status_code=HTTPStatus.SEE_OTHER
    )


@app.get('/search-travel', response_class=HTMLResponse)
def search_travel(
    request: Request,
    session: Session,  # type: ignore
):
    user = get_current_user(request, session)
    error = request.session.pop('error', None)
    return templates.TemplateResponse(
        request=request,
        name='search-travel.html',
        context={'user': user, 'error': error},
    )


@app.get('/profile/my-travels', response_class=HTMLResponse)
def previous_travels(
    request: Request,
    session: Session,  # type: ignore
):
    if user := get_current_user(request, session):
        return templates.TemplateResponse(
            name='profile/my-travels.html',
            context={'request': request, 'user': user},
        )
    return RedirectResponse(url='/sign-in', status_code=HTTPStatus.SEE_OTHER)


@app.get('/trip-participants/{travel_id}', response_class=HTMLResponse)
def trip_participants(
    request: Request,
    travel_id: int,  # Captura o travel_id da URL
    session: Session,  # type: ignore
):
    if user := get_current_user(request, session):
        # Por enquanto, não estamos utilizando o travel_id
        return templates.TemplateResponse(
            name='trip-participants.html',
            context={'request': request, 'user': user, 'travel_id': travel_id},
        )
    return RedirectResponse(url='/sign-in', status_code=HTTPStatus.SEE_OTHER)


@app.get('/sign-up', response_class=HTMLResponse)
def form_sign_up(request: Request):
    return templates.TemplateResponse(request=request, name='sign-up.html')


@app.get('/sign-in', response_class=HTMLResponse)
def form_sign_in(request: Request):
    error = request.session.pop('error', None)
    return templates.TemplateResponse(
        request=request, name='sign-in.html', context={'error': error}
    )


@app.get('/create-driver', response_class=HTMLResponse)
def create_driver(
    request: Request,
    session: Session,  # type: ignore
):
    if user := get_current_user(request, session):
        return templates.TemplateResponse(
            request=request, name='create-driver.html', context={'user': user}
        )
    return RedirectResponse(url='/sign-in', status_code=HTTPStatus.SEE_OTHER)


@app.get('/car', response_class=HTMLResponse)
def car(
    request: Request,
    session: Session,  # type: ignore
):
    user = get_current_user(request, session)
    driver = get_current_driver(request, session)
    if user and driver:
        return templates.TemplateResponse(
            request=request,
            name='car.html',
            context={'user': user, 'driver': driver},
        )
    return RedirectResponse(
        url='/create-driver', status_code=HTTPStatus.SEE_OTHER
    )


@app.get('/chats', response_class=HTMLResponse)
def my_chats(
    request: Request,
    session: Session,  # type: ignore
):
    user = get_current_user(request, session)
    if user:
        chat_list = chats.get_chats(session, user.id)
        return templates.TemplateResponse(
            request=request,
            name='chats.html',
            context={'user': user, 'chats': chat_list.chats},
        )
    return RedirectResponse(url='/sign-in', status_code=HTTPStatus.SEE_OTHER)
