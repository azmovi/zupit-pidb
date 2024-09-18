from http import HTTPStatus

from zupit.schemas.cars import Car
from zupit.schemas.travels import Address, TravelPublic
from zupit.schemas.users import Public


def test_create_travel(
    client,
    user: Public,
    car1: Car,
    origin: Address,
    middle: Address,
    destination: Address,
):
    data = {
        'user_id': user.id,
        'renavam': car1.renavam,
        'space': '4',
        'departure': '2025-10-11T11:00:00.000Z',
        'origin': {
            'user_id': origin.user_id,
            'direction': origin.direction,
            'cep': origin.cep,
            'street': origin.street,
            'district': origin.district,
            'city': origin.city,
            'state': origin.state,
            'house_number': origin.house_number,
        },
        'middle': {
            'user_id': middle.user_id,
            'direction': middle.direction,
            'cep': middle.cep,
            'street': middle.street,
            'district': middle.district,
            'city': middle.city,
            'state': middle.state,
            'house_number': middle.house_number,
        },
        'destination': {
            'user_id': destination.user_id,
            'direction': destination.direction,
            'cep': destination.cep,
            'street': destination.street,
            'district': destination.district,
            'city': destination.city,
            'state': destination.state,
            'house_number': destination.house_number,
        },
    }

    response = client.post('/travels', json=data)

    assert response.template.name == 'profile/index.html'
    assert response.status_code == HTTPStatus.OK


def test_create_same_travel(
    client,
    user: Public,
    car1: Car,
    origin: Address,
    middle: Address,
    destination: Address,
    travel: TravelPublic,
):
    data = {
        'user_id': user.id,
        'renavam': car1.renavam,
        'space': '4',
        'departure': '2025-10-11T10:00:00.000Z',
        'origin': {
            'user_id': origin.user_id,
            'direction': origin.direction,
            'cep': origin.cep,
            'street': origin.street,
            'district': origin.district,
            'city': origin.city,
            'state': origin.state,
            'house_number': origin.house_number,
        },
        'middle': {
            'user_id': middle.user_id,
            'direction': middle.direction,
            'cep': middle.cep,
            'street': middle.street,
            'district': middle.district,
            'city': middle.city,
            'state': middle.state,
            'house_number': middle.house_number,
        },
        'destination': {
            'user_id': destination.user_id,
            'direction': destination.direction,
            'cep': destination.cep,
            'street': destination.street,
            'district': destination.district,
            'city': destination.city,
            'state': destination.state,
            'house_number': destination.house_number,
        },
    }

    response = client.post('/travels', json=data)

    assert response.template.name == 'profile/index.html'
    assert response.status_code == HTTPStatus.OK


def test_get_travels_from_user(client, full_travel):
    response = client.get('/travels/1')
    travels = [TravelPublic.model_validate(full_travel).model_dump()]
    del travels[0]['arrival']
    del travels[0]['departure']

    resposta = response.json()
    resposta.get('travels')[0].pop('arrival')
    resposta.get('travels')[0].pop('departure')

    assert resposta == {'travels': travels}


def test_search_travel(
    client, travel: TravelPublic, full_travel: TravelPublic
):
    payload = {
        'leaving': travel.origin.address.city,
        'going': full_travel.middle.address.city
        if full_travel.middle
        else 'deu ruimk',
        'day': travel.departure.date(),
    }

    response = client.post('travels/search-travels', data=payload)
    assert response.status_code == HTTPStatus.OK
