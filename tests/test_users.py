from zupit.router.users import get_user
from zupit.schemas.users import Public


def test_create_brazilian(client):
    esperado = {
        'name': 'antonio',
        'email': 'antonio@example.com',
        'birthday': '2000-01-01',
        'sex': 'MAN',
        'passenger_rating': 0,
        'icon': None,
    }
    payload = {
        **esperado,
        'password': '123',
        'nationality': 'BRAZILIAN',
        'cpf': '12345678900',
    }

    response = client.post('/users', data=payload)

    user_db = response.context['user']
    user = Public(**esperado, doc=payload['cpf'], id=user_db.id)

    assert response.template.name == 'search-travel.html'
    assert user_db == user


def test_create_foreigner(client, session):
    esperado = {
        'name': 'antonio',
        'email': 'antonio@example.com',
        'birthday': '2000-01-01',
        'sex': 'MAN',
        'passenger_rating': 0,
        'icon': None,
    }
    payload = {
        **esperado,
        'password': '123',
        'nationality': 'FOREIGNER',
        'rnm': '02140873',
    }

    response = client.post('/users', data=payload)

    id = response.context['request'].session['id']
    user_db = get_user(id, session)
    user = Public(**esperado, doc=payload['rnm'], id=id)

    assert response.template.name == 'search-travel.html'
    assert user_db == user


def test_error_create_user_existent(client, user):
    payload = {
        'name': user.name,
        'email': user.email,
        'password': '123',
        'birthday': '2002-07-08',
        'sex': user.sex.value,
        'cpf': user.doc,
        'nationality': 'BRAZILIAN',
    }
    response = client.post('/users', data=payload)

    request = response.context.get('request', None)
    error = request.session.get('error', None)

    assert response.template.name == 'sign-up.html'
    assert error == 'User already exists'


def test_create_user_invalid(client):
    payload = {
        'name': 'antonio',
        'email': 'antonio@example.com',
        'birthday': '2000-01-01',
        'sex': 'MAN',
        'cpf': '12345678900',
        'password': '123',
        'nationality': 'FOREIGNER',
    }

    response = client.post('/users', data=payload)

    request = response.context.get('request', None)
    error = request.session.get('error', None)

    assert error == 'Input invalid'
    assert response.template.name == 'sign-up.html'


def test_confirm_user_credentials(client, user):
    payload = {
        'email': user.email,
        'password': '123',
    }

    response = client.post('/users/confirm-user', data=payload)
    user_db = response.context.get('user', None)

    assert user_db == user
    assert response.template.name == 'search-travel.html'


def test_wrong_emai_user_credentials(client, user):
    payload = {
        'email': 'wrongemail@example.com',
        'password': '123',
    }
    response = client.post('/users/confirm-user', data=payload)

    request = response.context.get('request', None)
    request.session.get('error', None)

    assert response.template.name == 'sign-in.html'


def test_wrong_password_user_credentials(client, user):
    payload = {
        'email': user.email,
        'password': 'wrongpassword',
    }

    response = client.post('/users/confirm-user', data=payload)

    request = response.context.get('request', None)
    request.session.get('error', None)

    assert response.template.name == 'sign-in.html'


def test_get_user_from_db(client, user):
    response = client.get(f'users/{user.id}')

    assert Public(**response.json()) == user


def test_get_user_not_exists(client):
    response = client.get('users/1')

    assert response.json() is None


def test_user_is_driver(client, user, driver):
    response = client.get(f'users/is_driver/{user.id}')

    assert response.json()


def test_user_is_not_driver(client, user):
    response = client.get(f'users/is_driver/{user.id}')

    assert not response.json()
