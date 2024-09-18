from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator

from zupit.utils import get_distance


class Address(BaseModel):
    id: Optional[int] = None
    cep: str
    street: str
    district: str
    city: str
    state: str
    house_number: str
    direction: Optional[str] = Field(default=None)
    user_id: Optional[int] = Field(default=None)


class Travel(BaseModel):
    id: Optional[int] = Field(default=None)
    user_id: int
    renavam: str
    space: int
    departure: datetime
    origin: Address
    middle: Optional[Address] = Field(default=None)
    destination: Address
    middle_distance: Optional[str] = Field(default=None)
    middle_duration: Optional[int] = Field(default=None)
    destination_distance: Optional[str] = Field(default=None)
    destination_duration: Optional[int] = Field(default=None)

    @model_validator(mode='after')
    def calculate_metrics(self):
        origin = self.origin.cep
        middle = None
        if self.middle:
            middle = self.middle.cep
        destination = self.destination.cep

        result = get_distance(origin, destination, middle)
        if result:
            if middle_results := result.get('middle', None):
                self.middle_distance, self.middle_duration = middle_results
            if destination_results := result.get('destination', None):
                (
                    self.destination_distance,
                    self.destination_duration,
                ) = destination_results
        else:
            raise ValueError('Invalid cep')
        return self


class Origin(BaseModel):
    space: int
    address: Address


class Middle(BaseModel):
    space: int
    duration: int
    distance: str
    price: float
    address: Address


class Destination(BaseModel):
    duration: int
    distance: str
    price: float
    address: Address


class TravelPublic(BaseModel):
    id: int
    status: bool
    user_id: int
    renavam: str
    departure: datetime
    origin: Origin
    middle: Optional[Middle] = Field(default=None)
    destination: Destination
    arrival: datetime
    involved: list[int]


class TravelList(BaseModel):
    travels: list[TravelPublic]
