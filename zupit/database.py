from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DATABASE_URL = (
    'postgresql+psycopg://postgres:postgres@zupit_database:5432/zupit_db'
)
engine = create_engine(DATABASE_URL)


def get_session() -> Generator[Session, None, None]:  # pragma: no cover
    with Session(engine) as session:
        yield session
