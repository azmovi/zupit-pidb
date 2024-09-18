from datetime import date
from enum import Enum
from typing import Optional, Union

from fastapi import Form
from pydantic import BaseModel, EmailStr


class Gender(Enum):
    MAN = 'MAN'
    WOMAN = 'WOMAN'


class Nationality(Enum):
    BRAZILIAN = 'BRAZILIAN'
    FOREIGNER = 'FOREIGNER'


class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    birthday: date
    sex: Gender
    nationality: Nationality
    cpf: Optional[str] = None
    rnm: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        birthday: str = Form(...),
        sex: str = Form(...),
        nationality: str = Form(...),
        cpf: str = Form(None),
        rnm: str = Form(None),
    ):
        return cls(
            name=name,
            email=email,
            password=password,
            birthday=date.fromisoformat(birthday),
            sex=Gender(sex),
            nationality=Nationality(nationality),
            cpf=cpf,
            rnm=rnm,
        )


class Public(BaseModel):
    id: int
    name: str
    email: EmailStr
    birthday: date
    sex: Gender
    icon: Optional[bytes]
    passenger_rating: float
    doc: str


class Brazilian(BaseModel):
    id: int
    name: str
    email: EmailStr
    birthday: date
    sex: Gender
    icon: Optional[bytes] = None
    passenger_rating: float
    cpf: str


class Foreigner(BaseModel):
    id: int
    name: str
    email: EmailStr
    birthday: date
    sex: Gender
    icon: Optional[bytes] = None
    passenger_rating: float
    rnm: str


class UserCredentials(BaseModel):
    email: str
    password: str

    @classmethod
    def as_form(
        cls,
        email: str = Form(),
        password: str = Form(),
    ):
        return cls(
            email=email,
            password=password,
        )


UserPublic = Union[Brazilian, Foreigner, Public]
