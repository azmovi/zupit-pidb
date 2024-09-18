from http import HTTPStatus
from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.cars import Car, CarList


def create_car_db(car: Car, session: Session = Depends(get_session)) -> bool:
    sql = text(
        """
        SELECT * FROM create_car(
            :renavam, :user_id, :brand, :model, :plate, :color
        );
        """
    )
    try:
        result = session.execute(
            sql,
            {
                'renavam': car.renavam,
                'user_id': car.user_id,
                'brand': car.brand,
                'model': car.model,
                'plate': car.plate,
                'color': car.color,
            },
        )
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
        )
    return bool(result)


def get_car_db(renavam: str, session: Session) -> Optional[Car]:
    sql = text('SELECT * FROM get_car_by_renavam(:renavam);')

    car_db = session.execute(sql, {'renavam': renavam}).fetchone()
    session.commit()

    if car_db:
        return Car(
            renavam=car_db[0],
            user_id=car_db[1],
            brand=car_db[2],
            model=car_db[3],
            plate=car_db[4],
            color=car_db[5],
        )
    return None


def get_cars_db(
    user_id: int, session: Session = Depends(get_session)
) -> CarList:
    car_list = []
    sql = text(' SELECT * FROM get_cars_by_user_id(:user_id)')
    cars = session.execute(sql, {'user_id': user_id}).fetchall()
    for car in cars:
        car_exemple = Car(
            renavam=car[0],
            user_id=car[1],
            brand=car[2],
            model=car[3],
            plate=car[4],
            color=car[5],
        )
        car_list.append(car_exemple)

    return CarList(cars=car_list)
