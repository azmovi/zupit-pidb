from fastapi import Form
from pydantic import BaseModel


class Car(BaseModel):
    renavam: str
    user_id: int
    brand: str
    model: str
    plate: str
    color: str

    @classmethod
    def as_form(
        cls,
        renavam: str = Form(...),
        user_id: int = Form(...),
        brand: str = Form(...),
        model: str = Form(...),
        plate: str = Form(...),
        color: str = Form(...),
    ):
        return cls(
            renavam=renavam,
            user_id=user_id,
            brand=brand,
            model=model,
            plate=plate,
            color=color,
        )


class CarPublic(BaseModel):
    renavam: str
    user_id: int
    brand: str
    model: str
    plate: str
    color: str


class CarList(BaseModel):
    cars: list[Car]
