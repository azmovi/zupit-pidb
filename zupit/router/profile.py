from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.utils import get_current_user

templates = Jinja2Templates(directory='zupit/templates')
router = APIRouter(prefix='/profile', tags=['profile'])


@router.get('/', response_class=HTMLResponse)
def index(
    request: Request,
    session: Session = Depends(get_session),  # type: ignore
):
    user = get_current_user(request, session)
    if user:
        return templates.TemplateResponse(
            request=request,
            name='profile/index.html',
            context={'user': user},
        )
    return RedirectResponse(url='/sign-up', status_code=HTTPStatus.SEE_OTHER)


@router.get('/view/{user_id}', response_class=HTMLResponse)
def view_by_user(
    request: Request,
    user_id: int,
    session: Session = Depends(get_session),  # type: ignore
):
    user = get_current_user(
        request, session
    )  # Assuming this is a helper function in your code
    error = request.session.get('error', None)
    if user:
        return templates.TemplateResponse(
            name='profile/view.html',  # Path to the template
            context={
                'request': request,
                'user': user,
                'user_id': user_id,
                'error': error,
            },
        )
    return RedirectResponse(
        url='/profile/my-travels', status_code=HTTPStatus.SEE_OTHER
    )


# @router.get('/{step}', response_class=HTMLResponse)
# def step(
#     request: Request,
#     session: Session,  # type: ignore
#     step: str,
# ):
#     user = get_current_user(request, session)
#     driver = get_current_driver(request, session)
#     if user and driver:
#         return templates.TemplateResponse(
#             request=request,
#             name=f'offer/{step}.html',
#             context={'user': user, 'driver': driver},
#         )
#     return RedirectResponse(
#         url='/create-driver', status_code=HTTPStatus.SEE_OTHER
#     )
