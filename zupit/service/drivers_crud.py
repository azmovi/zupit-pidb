from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from zupit.schemas.drivers import Driver


def create_driver_db(driver: Driver, session: Session):
    sql = text('SELECT * FROM create_driver(:user_id, :cnh, :preferences)')

    try:
        session.execute(
            sql,
            {
                'user_id': driver.user_id,
                'cnh': driver.cnh,
                'preferences': driver.preferences,
            },
        )
        session.commit()

    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
        )


def get_driver_db(user_id: int, session: Session) -> Optional[Driver]:
    sql = text('SELECT * FROM get_driver(:user_id);')
    driver_db = session.execute(sql, {'user_id': user_id}).fetchone()
    session.commit()

    if driver_db:
        return Driver(
            cnh=driver_db[0],
            user_id=driver_db[1],
            rating=driver_db[2],
            preferences=driver_db[3],
        )
    return None
