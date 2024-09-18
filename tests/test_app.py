from http import HTTPStatus


def test_reset_session(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'search-travel.html'


def test_search_travel_html(client):
    response = client.get('/search-travel')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'search-travel.html'


def test_form_sign_up_html(client):
    response = client.get('/sign-up')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'sign-up.html'


def test_form_sign_in_html(client):
    response = client.get('/sign-in')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'sign-in.html'


def test_logoff_user(client):
    response = client.get('/logoff')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'search-travel.html'


def test_driver_html(client, user):
    response = client.get('/create-driver')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'create-driver.html'
    assert response.context['request'].session['id'] == user.id


def test_driver_html_without_user(client):
    response = client.get('/create-driver')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'sign-in.html'


def test_offer_html_with_driver(client, driver):
    response = client.get('/offer')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'offer/first.html'
    assert response.context['driver'] == driver


def test_offer_html_without_driver(client, user):
    response = client.get('/offer')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'create-driver.html'
    assert response.context['user'] == user


def test_offer_html_without_user(client):
    response = client.get('/offer')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'sign-in.html'


def test_car_html(client, driver):
    response = client.get('/car')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'car.html'
    assert response.context['driver'] == driver


def test_car_html_withou_driver(client, user):
    response = client.get('/car')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'create-driver.html'
    assert response.context['user'] == user


def test_car_html_withou_user(client):
    response = client.get('/car')

    assert response.status_code == HTTPStatus.OK
    assert response.template.name == 'sign-in.html'
