from zupit.schemas.cars import Car


def test_create_car(client, user, driver):
    car = {
        'renavam': '12345678900',
        'user_id': user.id,
        'brand': 'fiat',
        'model': 'mobi',
        'plate': 'fjr5231',
        'color': 'vermelho',
    }

    response = client.post('/cars', data=car)
    assert response.template.name == 'offer/first.html'


def test_create_same_car(client, user, driver, car1):
    car = {
        'renavam': car1.renavam,
        'user_id': user.id,
        'brand': car1.brand,
        'model': car1.model,
        'plate': car1.plate,
        'color': car1.color,
    }

    response = client.post('/cars', data=car)

    request = response.context.get('request', None)
    user_db = response.context.get('user', None)
    error = request.session.get('error', None)

    assert user_db == user
    assert response.template.name == 'car.html'
    assert error == 'Car already exists'


def test_create_invalid_car(client, user, driver, car1):
    car = {
        'renavam': '3123123122313',
        'user_id': user.id,
        'brand': car1.brand,
        'model': car1.model,
        'plate': car1.plate,
        'color': car1.color,
    }

    response = client.post('/cars', data=car)

    request = response.context.get('request', None)
    user_db = response.context.get('user', None)
    error = request.session.get('error', None)

    assert user_db == user
    assert response.template.name == 'car.html'
    assert error == 'Input invalid'


def test_list_car_of_user(client, user, car1, car2):
    response = client.get(f'/cars/{user.id}')
    cars = [Car.model_validate(car).model_dump() for car in [car1, car2]]
    assert response.json() == {'cars': cars}


def test_list_car_of_invalid_user(client, user, car1):
    response = client.get(f'/cars/{user.id + 1}')
    assert response.json() == {'cars': []}
