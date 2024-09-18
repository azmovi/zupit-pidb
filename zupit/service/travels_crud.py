from datetime import date
from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.travels import (
    Address,
    Destination,
    Middle,
    Origin,
    Travel,
    TravelList,
    TravelPublic,
)

Session = Annotated[Session, Depends(get_session)]


def create_address_db(
    session: Session,  # type: ignore
    address: Address,
) -> int:
    sql = text(
        """SELECT * FROM create_address(
            :cep,
            :street,
            :city,
            :state,
            :district,
            :house_number,
            :direction,
            :user_id
        )"""
    )
    address_dict = address.model_dump()
    try:
        result = session.execute(sql, address_dict)
        address_id = result.fetchone()[0]
        session.commit()
        if address_id:
            return address_id
        else:
            session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.NOT_ACCEPTABLE,
                detail='Address not create',
            )
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
        )


def get_address_db(
    session: Session,  # type: ignore
    address_id: int,
) -> Address:
    sql = text('SELECT * FROM get_address_by_id(:id)')
    try:
        result = session.execute(sql, {'id': address_id})
        address_db = result.fetchone()
        session.commit()
        if address_db:
            return Address(
                id=address_db[0],
                cep=address_db[1],
                street=address_db[2],
                city=address_db[3],
                state=address_db[4],
                district=address_db[5],
                house_number=address_db[6],
                direction=address_db[7],
                user_id=address_db[8],
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Address not found',
            )
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
        )


def create_travel_db(
    session: Session,  # type: ignore
    travel: Travel,
) -> int:
    middle_address_id = None
    origin_address_id = create_address_db(session, travel.origin)
    if travel.middle:
        middle_address_id = create_address_db(session, travel.middle)
    destination_address_id = create_address_db(session, travel.destination)

    sql = text(
        """
        SELECT * FROM create_travel(
            :user_id,
            :renavam,
            :space,
            :departure,
            :origin_address_id,
            :middle_address_id,
            :middle_duration,
            :middle_distance,
            :destination_address_id,
            :destination_duration,
            :destination_distance
        )
        """
    )
    try:
        result = session.execute(
            sql,
            {
                'user_id': travel.user_id,
                'renavam': travel.renavam,
                'space': travel.space,
                'departure': travel.departure,
                'origin_address_id': origin_address_id,
                'middle_address_id': middle_address_id,
                'middle_duration': travel.middle_duration,
                'middle_distance': travel.middle_distance,
                'destination_address_id': destination_address_id,
                'destination_duration': travel.destination_duration,
                'destination_distance': travel.destination_distance,
            },
        )
        id = result.fetchone()[0]
        session.commit()
        return id
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Travel creation Invalid',
        )


def get_travel_db(
    session: Session,  # type: ignore
    id: int,
) -> Optional[TravelPublic]:
    sql = text('SELECT * FROM get_travel(:id)')
    result = session.execute(sql, {'id': id}).fetchone()
    session.commit()
    return make_travel_public(result)


def get_travel_by_user(
    session: Session,  # type: ignore
    user_id: int,
):
    sql = text('SELECT * FROM get_travel_by_user(:user_id)')
    travels = session.execute(sql, {'user_id': user_id}).fetchall()
    list_travel = []
    for travel in travels:
        list_travel.append(make_travel_public(travel))
    return TravelList(travels=list_travel)


def search_travel_db(
    session: Session,  # type: ignore
    leaving: str,
    going: str,
    day: date,
) -> TravelList:
    sql = text('SELECT * FROM search_travel(:leaving, :going, :day)')
    try:
        travels = session.execute(
            sql, {'leaving': leaving, 'going': going, 'day': day}
        ).fetchall()
        list_travel = [make_travel_public(travel) for travel in travels]
        return TravelList(travels=list_travel)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


def confirm_travel_db(
    session: Session,  # type: ignore
    user_id: int,
    travel_id: int,
):
    sql = text('SELECT * FROM confirm_travel(:user_id, :travel_id)')
    try:
        session.execute(sql, {'user_id': user_id, 'travel_id': travel_id})
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Você não pode pegar essa viagem',
        )


def make_travel_public(result) -> TravelPublic:
    return TravelPublic(
        id=result[0],
        status=result[1],
        user_id=result[2],
        renavam=result[3],
        departure=result[4],
        origin=Origin(
            space=result[5],
            address=Address(
                cep=result[6],
                street=result[7],
                city=result[8],
                state=result[9],
                district=result[10],
                house_number=result[11],
            ),
        ),
        middle=Middle(
            space=result[12],
            duration=result[13],
            distance=result[14],
            price=result[15],
            address=Address(
                cep=result[16],
                street=result[17],
                city=result[18],
                state=result[19],
                district=result[20],
                house_number=result[21],
            ),
        )
        if result[12] is not None
        else None,
        destination=Destination(
            duration=result[22],
            distance=result[23],
            price=result[24],
            address=Address(
                cep=result[25],
                street=result[26],
                city=result[27],
                state=result[28],
                district=result[29],
                house_number=result[30],
            ),
        ),
        arrival=result[31],
        involved=result[32],
    )
