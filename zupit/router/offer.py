from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.utils import get_current_driver, get_current_user

templates = Jinja2Templates(directory='zupit/templates')
router = APIRouter(prefix='/offer', tags=['offer'])

Session = Annotated[Session, Depends(get_session)]


@router.get('/', response_class=HTMLResponse)
def first(
    request: Request,
    session: Session,  # type: ignore
):
    user = get_current_user(request, session)
    driver = get_current_driver(request, session)
    error = request.session.get('error', None)
    if user and driver:
        return templates.TemplateResponse(
            request=request,
            name='offer/first.html',
            context={'user': user, 'driver': driver, 'error': error},
        )
    return RedirectResponse(
        url='/create-driver', status_code=HTTPStatus.SEE_OTHER
    )


@router.get('/{step}', response_class=HTMLResponse)
def step(
    request: Request,
    session: Session,  # type: ignore
    step: str,
):
    user = get_current_user(request, session)
    driver = get_current_driver(request, session)
    error = request.session.get('error', None)
    if user and driver:
        return templates.TemplateResponse(
            request=request,
            name=f'offer/{step}.html',
            context={'user': user, 'driver': driver, 'error': error},
        )
    return RedirectResponse(
        url='/create-driver', status_code=HTTPStatus.SEE_OTHER
    )
