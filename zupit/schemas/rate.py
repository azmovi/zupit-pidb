from enum import Enum
from typing import Optional

from fastapi import Form
from pydantic import BaseModel


class rating_type(Enum):
    CARONISTA = 'CARONISTA'
    CARONEIRO = 'CARONEIRO'


class rating_grade(Enum):
    PESSIMO = 'PESSIMO'
    RUIM = 'RUIM'
    MEDIANO = 'MEDIANO'
    BOM = 'BOM'
    OTIMO = 'OTIMO'


class Rate(BaseModel):
    author_id: int
    recipient_id: int
    rate_type: rating_type
    grade: rating_grade
    content: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        author_id: int = Form(...),
        recipient_id: int = Form(...),
        rate_type: str = Form(...),
        grade: str = Form(...),
        content: Optional[str] = Form(None),
    ):
        return cls(
            author_id=author_id,
            recipient_id=recipient_id,
            rate_type=rating_type(rate_type),
            grade=rating_grade(grade),
            content=content,
        )


class RatePublic(BaseModel):
    author_id: int
    recipient_id: int
    rate_type: rating_type
    grade: rating_grade
    content: Optional[str] = None


class RateList(BaseModel):
    rates: list[RatePublic]