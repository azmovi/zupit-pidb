from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.drivers import Driver
from zupit.service.drivers_crud import create_driver_db, get_driver_db

router = APIRouter(prefix='/drivers', tags=['drivers'])


@router.post(
    '/',
    response_class=HTMLResponse,
    status_code=HTTPStatus.CREATED,
)
def create_driver(
    request: Request,
    session: Session = Depends(get_session),
    driver: Driver = Depends(Driver.as_form),
) -> RedirectResponse:
    try:
        driver_db = get_driver_db(driver.user_id, session)
        if driver_db:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Driver already exists'
            )
        create_driver_db(driver, session)
        request.session['driver'] = True
        return RedirectResponse(url='/offer', status_code=HTTPStatus.SEE_OTHER)

    except HTTPException as exc:
        request.session['error'] = exc.detail
        return RedirectResponse(
            url='/create-driver', status_code=HTTPStatus.SEE_OTHER
        )


@router.get('/{user_id}', response_model=Driver)
def get_driver(user_id: int, session: Session = Depends(get_session)):
    db_user = get_driver_db(user_id, session)
    if db_user:
        return db_user
    return JSONResponse(
        status_code=404, content={'message': 'Nenhum motorista encontrado.'}
    )
