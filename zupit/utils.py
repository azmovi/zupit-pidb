from typing import Annotated, Optional

from fastapi import Depends, Request
from googlemaps import Client
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.router.drivers import get_driver
from zupit.router.users import get_user
from zupit.schemas.drivers import Driver
from zupit.schemas.users import UserPublic
from zupit.settings import Settings

Session = Annotated[Session, Depends(get_session)]


def get_current_user(
    request: Request,
    session: Session,  # type: ignore
) -> Optional[UserPublic]:
    if id := request.session.get('id', None):
        return get_user(id, session)
    return None


def get_current_driver(
    request: Request,
    session: Session,  # type: ignore
) -> Optional[Driver]:
    if id := request.session.get('id'):
        if driver := get_driver(id, session):
            return driver
    return None


def get_outputs(origin: str, destination: str) -> Optional[tuple[str, int]]:
    app = Client(Settings().API_KEY)  # type: ignore

    data = app.distance_matrix(  # type: ignore
        origins=origin, destinations=destination, mode='driving'
    )
    if data:
        rows = data.get('rows')[0]
        elements = rows.get('elements')[0]
        if elements.get('status') == 'OK':
            distance = elements.get('distance').get('text')
            duration = elements.get('duration').get('value')
            return distance, duration
    return None


def get_distance(
    origin: str, destination: str, middle: Optional[str]
) -> Optional[dict[str, tuple[str, int]]]:
    """
    {'middle': ('235 km', 10612), 'destination': ('76.2 km', 5977)}
    {'destination': ('331 km', 15937)}
    """
    result = {}
    if middle:
        if results := get_outputs(origin, middle):
            result['middle'] = results
        if results := get_outputs(middle, destination):
            result['destination'] = results
    elif results := get_outputs(origin, destination):
        result['destination'] = results

    return result
