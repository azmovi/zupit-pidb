from http import HTTPStatus
from typing import Optional, Union

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from zupit.schemas.users import (
    Gender,
    Public,
    User,
    UserCredentials,
)


def create_user_db(user: User, session: Session) -> int:
    if user.nationality.value == 'BRAZILIAN':
        doc = user.cpf
        sql = text(
            """
            SELECT * FROM create_brazilian(
                :name, :email, :password, :birthday, :sex, :doc
            );
            """
        )
    else:
        doc = user.rnm
        sql = text(
            """
            SELECT id FROM create_foreigner(
                :name, :email, :password, :birthday, :sex, :doc
            );
            """
        )
    try:
        result = session.execute(
            sql,
            {
                'name': user.name,
                'email': user.email,
                'password': user.password,
                'birthday': user.birthday,
                'sex': user.sex.value,
                'doc': doc,
            },
        ).fetchone()
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
        )
    if result:
        return result[0]  # id

    else:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='User creation failed'
        )


def get_user_db(campo: Union[str, int], session: Session) -> Optional[Public]:
    if isinstance(campo, int):
        sql = text('SELECT * FROM get_user_by_id(:campo);')
    elif isinstance(campo, str):
        sql = text('SELECT * FROM get_user_by_email(:campo);')

    result = session.execute(sql, {'campo': campo})
    user_db = result.fetchone()
    session.commit()

    if user_db:
        return Public(
            id=user_db[0],
            name=user_db[1],
            email=user_db[2],
            birthday=user_db[3],
            sex=Gender(user_db[4]),
            icon=user_db[5],
            passenger_rating=user_db[6],
            doc=user_db[7],
        )
    return None


def confirm_user_db(user: UserCredentials, session: Session) -> int:
    sql = text('SELECT id FROM confirm_user(:email, :password);')
    try:
        user_db = session.execute(
            sql, {'email': user.email, 'password': user.password}
        ).fetchone()
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    if user_db:
        return user_db[0]  # id do user
    else:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid credentials'
        )
