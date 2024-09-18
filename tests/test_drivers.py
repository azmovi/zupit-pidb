def test_create_driver_without_preferences(client, user):
    driver = {
        'cnh': '123456789',
        'user_id': user.id,
        'preferences': None,
    }

    response = client.post('/drivers', data=driver)

    assert response.template.name == 'offer/first.html'
    assert response.context['driver']


def test_create_driver_with_preferences(client, user):
    driver = {
        'user_id': user.id,
        'cnh': '123456789',
        'preferences': 'Gosto de cachorro quente',
    }

    response = client.post('/drivers', data=driver)

    assert response.template.name == 'offer/first.html'
    assert response.context['driver']


def test_create_same_driver(client, user, driver):
    driver = {
        'user_id': user.id,
        'cnh': driver.cnh,
        'preferences': driver.preferences,
    }

    response = client.post('/drivers', data=driver)

    request = response.context.get('request', None)
    user_db = response.context.get('user', None)
    error = request.session.get('error', None)

    assert response.template.name == 'create-driver.html'
    assert user_db == user
    assert error == 'Driver already exists'


def test_create_invalid_driver(client, user):
    driver = {
        'user_id': user.id + 1,
        'cnh': '123456789',
        'preferences': 'xpto',
    }

    response = client.post('/drivers', data=driver)

    request = response.context.get('request', None)
    user_db = response.context.get('user', None)
    error = request.session.get('error', None)

    assert response.template.name == 'create-driver.html'
    assert user_db == user
    assert error == 'Input invalid'
