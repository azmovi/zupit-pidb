\c zupit_db

SELECT create_brazilian(
    'Antonio',
    'a@a.com',
    '123',
    '1990-05-15',
    'MAN',
    '12345678901'
);

SELECT create_brazilian(
    'Vitor',
    'vitor@email.com',
    '456',
    '2000-05-15',
    'MAN',
    '12345678902'
);

SELECT create_foreigner(
    'Maria Gonzalez',
    'maria@example.com',
    'senha456',
    '1985-09-10',
    'WOMAN',
    'A1234567'
);

SELECT create_foreigner(
    'Ze Gonzalez',
    'ze@example.com',
    'senha123',
    '1995-09-10',
    'MAN',
    'B1234567'
);

SELECT create_driver(
    1,
    '98765432100',
    'Prefere não fumar no carro'
);

SELECT create_car(
    '00123456789',
    1,
    'Toyota',
    'Corolla',
    'XYZ1234',
    'Preto'
);

SELECT create_address(
    '12345-678',
    'Rua Principal',
    'Cidade Exemplo',
    'EX',
    'Bairro Central',
    '10',
    'PICK_UP',
    1
);

SELECT create_address(
    '23456-789',
    'Avenida Secundária',
    'Cidade Intermediária',
    'EX',
    'Bairro Intermediário',
    '25',
    'MIDDLE',
    1
);

SELECT create_address(
    '34567-890',
    'Rua Final',
    'Cidade Destino',
    'EX',
    'Bairro Final',
    '30',
    'PICK_OFF',
    1
);

SELECT create_travel(
    1,
    '00123456789',
    2,
    '2024-10-15 08:00:00+00',
    (SELECT id FROM address WHERE cep = '12345-678'),
    (SELECT id FROM address WHERE cep = '23456-789'),
    3600,
    '10km',
    (SELECT id FROM address WHERE cep = '34567-890'),
    1800,
    '20km'
);

SELECT create_travel(
    1,
    '00123456789',
    2,
    '2024-9-16 08:00:00+00',
    (SELECT id FROM address WHERE cep = '12345-678'),
    (SELECT id FROM address WHERE cep = '23456-789'),
    3600,
    '10km',
    (SELECT id FROM address WHERE cep = '34567-890'),
    1800,
    '20km'
);

SELECT confirm_travel(
    2,
    2
);

SELECT confirm_travel(
    3,
    1
);

SELECT confirm_travel(
    4,
    2
);

SELECT create_or_update_rating(
    2,
    1,
    'CARONISTA',
    'BOM',
    'Achei bem dos bons'
);

SELECT create_or_update_rating(
    2,
    1,
    'CARONEIRO',
    'OTIMO',
    NULL
);

SELECT create_or_update_rating(
    3,
    1,
    'CARONISTA',
    'MEDIANO',
    'Achei médio'
);

