from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from zupit.schemas.rate import Rate, RateList, RatePublic


def create_rating_db(rating: Rate, session: Session):
    sql = text(
        """
        SELECT * FROM create_or_update_rating(
            :author_id, :recipient_id, :rate_type, :grade, :content
        )"""
    )

    try:
        session.execute(
            sql,
            {
                'author_id': rating.author_id,
                'recipient_id': rating.recipient_id,
                'rate_type': rating.rate_type.value,
                'grade': rating.grade.value,
                'content': rating.content,
            },
        )
        session.commit()

    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
        )


def get_rating_db(id: int, session: Session) -> Optional[Rate]:
    sql = text(
        """
        SELECT id, author_id, id, rate_type, grade, content, creation
        FROM get_rating_by_id(:id);
        """
    )
    rate_db = session.execute(sql, {'id': id}).fetchone()
    session.commit()

    if rate_db:
        return Rate(
            id=rate_db[0],
            author_id=rate_db[1],
            recipient_id=rate_db[2],
            rate_type=rate_db[3],
            grade=rate_db[4],
            content=rate_db[5],
            creation=rate_db[6],
        )
    return None


def get_rates_by_user(
    session: Session,  # type: ignore
    recipient_id: int,
):
    sql = text('SELECT * FROM get_rates_by_user(:recipient_id)')
    list_rate = []
    rates = session.execute(sql, {'recipient_id': recipient_id}).fetchall()

    for rate in rates:
        rate_instance = RatePublic(
            id=rate[0],
            author_id=rate[1],
            recipient_id=rate[2],
            rate_type=rate[3],
            grade=rate[4],
            content=rate[5],
            creation=rate[6],
        )
        list_rate.append(rate_instance)

    return RateList(rates=list_rate)


def check_rating_db(
    recipient_id: int, author_id: int, rate_type: str, session: Session
) -> Optional[Rate]:
    sql = text(
        """
        SELECT id, author_id, recipient_id, rate_type, grade, content, creation
        FROM check_rating_exists(:author_id, :recipient_id, :rate_type);
        """
    )

    try:
        rate_db = session.execute(
            sql,
            {
                'author_id': author_id,
                'recipient_id': recipient_id,
                'rate_type': rate_type,
            },
        ).fetchone()
        session.commit()

        if rate_db:
            return Rate(
                id=rate_db[0],
                author_id=rate_db[1],
                recipient_id=rate_db[2],
                rate_type=rate_db[3],
                grade=rate_db[4],
                content=rate_db[5],
                creation=rate_db[6],
            )
        return None

    except Exception as e:
        session.rollback()
        print(f'Erro ao verificar a avaliação no banco de dados: {e}')
        return None