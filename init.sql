\c zupit_db

-----------------------------------------------------------------
---------------------------USUARIO-------------------------------
-----------------------------------------------------------------

CREATE TYPE gender AS ENUM ('MAN', 'WOMAN');

CREATE TYPE user_public AS (
    id INTEGER,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    sex gender,
    icon BYTEA,
    passenger_rating FLOAT,
    doc VARCHAR
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(32) NOT NULL,
    birthday DATE NOT NULL,
    sex gender NOT NULL,
    icon BYTEA,
    passenger_rating FLOAT NOT NULL,
    user_status BOOLEAN NOT NULL
);

CREATE TABLE brazilians (
    cpf VARCHAR(11) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE foreigners (
    rnm VARCHAR(8) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE FUNCTION create_user(
    p_name VARCHAR,
    p_email VARCHAR,
    p_password VARCHAR,
    p_birthday DATE,
    p_sex gender
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_user_id INTEGER;
BEGIN
    INSERT INTO users (name, email, password, birthday, sex, icon, passenger_rating, user_status)
    VALUES (p_name, p_email, p_password, p_birthday, p_sex, NULL, 0.0, TRUE)
    RETURNING id INTO v_user_id;

    RETURN v_user_id;
END;
$$;

CREATE FUNCTION _create_brazilian(
    p_cpf VARCHAR,
    p_id_user INTEGER
) RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO brazilians (cpf, user_id)
    VALUES (p_cpf, p_id_user);
END;
$$;


CREATE FUNCTION create_brazilian(
    p_name VARCHAR,
    p_email VARCHAR,
    p_password VARCHAR,
    p_birthday DATE,
    p_sex gender,
    p_cpf VARCHAR
) RETURNS SETOF user_public
LANGUAGE plpgsql
AS $$
DECLARE 
    v_user_id INTEGER;
BEGIN
    v_user_id := create_user(p_name, p_email, p_password, p_birthday, p_sex);

    PERFORM _create_brazilian(p_cpf, v_user_id);

    RETURN QUERY 
    SELECT 
        u.id, u.name, u.email, u.birthday, u.sex, u.icon, u.passenger_rating, b.cpf
    FROM 
        users u 
    LEFT JOIN 
        brazilians b ON u.id = b.user_id
    WHERE 
        u.id = v_user_id;
END;
$$;


CREATE FUNCTION _create_foreigner(
    p_rnm VARCHAR,
    p_id_user INTEGER
) RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO foreigners (rnm, user_id)
    VALUES (p_rnm, p_id_user);
END;
$$;

CREATE FUNCTION create_foreigner(
    p_name VARCHAR,
    p_email VARCHAR,
    p_password VARCHAR,
    p_birthday DATE,
    p_sex gender,
    p_rnm VARCHAR
) RETURNS SETOF user_public
LANGUAGE plpgsql
AS $$
DECLARE 
    v_user_id INTEGER;
BEGIN
    v_user_id := create_user(p_name, p_email, p_password, p_birthday, p_sex);
    PERFORM _create_foreigner(p_rnm, v_user_id);

    RETURN QUERY 
    SELECT 
        u.id, u.name, u.email, u.birthday, u.sex, u.icon, u.passenger_rating, f.rnm
    FROM 
        users u 
    LEFT JOIN 
        foreigners f ON u.id = v_user_id
    WHERE 
        u.id = v_user_id;
END;
$$;

CREATE FUNCTION get_user_doc(p_id INTEGER)
RETURNS VARCHAR
LANGUAGE plpgsql
AS $$
DECLARE
    doc VARCHAR;
BEGIN
    SELECT b.cpf INTO doc
    FROM brazilians b
    WHERE b.user_id = p_id
    LIMIT 1;

    IF doc IS NULL THEN
        SELECT f.rnm INTO doc
        FROM foreigners f
        WHERE f.user_id = p_id
        LIMIT 1;
    END IF;

    RETURN doc;
END;
$$;

CREATE FUNCTION get_user_by_id(p_id INTEGER)
RETURNS SETOF user_public
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT u.id,
           u.name,
           u.email,
           u.birthday,
           u.sex,
           u.icon,
           u.passenger_rating,
           get_user_doc(u.id)
    FROM users u
    WHERE u.id = p_id
    LIMIT 1;
END;
$$;

CREATE FUNCTION get_user_by_email(p_email VARCHAR)
RETURNS SETOF user_public
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT u.id,
           u.name,
           u.email,
           u.birthday,
           u.sex,
           u.icon,
           u.passenger_rating,
           get_user_doc(u.id)
    FROM users u
    WHERE u.email = p_email
    LIMIT 1;
END;
$$;

CREATE FUNCTION confirm_user(
    p_email VARCHAR,
    p_password VARCHAR
) RETURNS SETOF user_public
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT u.id,
           u.name,
           u.email,
           u.birthday,
           u.sex,
           u.icon,
           u.passenger_rating,
           get_user_doc(u.id)
    FROM users u
    WHERE u.email = p_email
    AND u.password = p_password
    LIMIT 1;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'User not found';
    END IF;
END;
$$;

-----------------------------------------------------------------
---------------------------Caronista-----------------------------
-----------------------------------------------------------------

CREATE TABLE drivers (
    cnh VARCHAR(11) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    rating FLOAT NOT NULL,
    preferences VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE FUNCTION create_driver(
    p_user_id INTEGER,
    p_cnh VARCHAR,
    p_preferences VARCHAR
) RETURNS SETOF drivers
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO drivers (cnh, user_id, rating, preferences)
    VALUES (p_cnh, p_user_id, 0, p_preferences);

    RETURN QUERY
    SELECT *
    FROM drivers
    WHERE user_id = p_user_id
    LIMIT 1;
END;
$$;

CREATE FUNCTION get_driver(p_user_id INTEGER)
RETURNS SETOF drivers
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM drivers
    WHERE user_id = p_user_id;
END;
$$;

CREATE TABLE cars (
    renavam VARCHAR(11) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    plate VARCHAR(7) NOT NULL,
    color VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE FUNCTION create_car(
    p_renavam VARCHAR(11),
    p_user_id INTEGER,
    p_brand VARCHAR(50),
    p_model VARCHAR(50),
    p_plate VARCHAR(7),
    p_color VARCHAR(50)
) RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO cars (renavam, user_id, brand, model, plate, color)
    VALUES (p_renavam, p_user_id, p_brand, p_model, p_plate, p_color);
END;
$$;

CREATE FUNCTION get_car_by_renavam(p_renavam VARCHAR)
RETURNS SETOF cars
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM cars
    WHERE renavam = p_renavam
    LIMIT 1;
END;
$$;

CREATE FUNCTION get_cars_by_user_id(p_user_id INTEGER)
RETURNS SETOF cars
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM cars
    WHERE user_id = p_user_id;
END;
$$;

-----------------------------------------------------------------
---------------------------VIAGEM--------------------------------
-----------------------------------------------------------------
CREATE TYPE direction AS ENUM ('PICK_UP', 'PICK_OFF', 'MIDDLE');

CREATE TABLE address (
    id SERIAL PRIMARY KEY NOT NULL,
    cep VARCHAR(9) NOT NULL,
    street VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(2) NOT NULL,
    district VARCHAR(50) NOT NULL,
    house_number VARCHAR(5) NOT NULL,
    direction direction NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE FUNCTION create_address(
    p_cep VARCHAR,
    p_street VARCHAR,
    p_city VARCHAR,
    p_state VARCHAR,
    p_district VARCHAR,
    p_house_number VARCHAR,
    p_direction direction,
    p_user_id INTEGER
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    address_id INTEGER;
BEGIN
    INSERT INTO address (cep, street, city, state, district, house_number, direction, user_id)
    VALUES (p_cep, p_street, p_city, p_state, p_district, p_house_number, p_direction, p_user_id)
    RETURNING id INTO address_id;

    RETURN address_id;
END;
$$;

CREATE FUNCTION get_address_by_id(
    p_id INTEGER
) RETURNS SETOF address
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM address
    WHERE id = p_id;
END;
$$;

CREATE TABLE origins (
    id SERIAL PRIMARY KEY,
    address_id INTEGER NOT NULL,
    space INTEGER NOT NULL,
    FOREIGN KEY (address_id) REFERENCES address(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE middles (
    id SERIAL PRIMARY KEY,
    address_id INTEGER NOT NULL,
    space INTEGER NOT NULL,
    duration INTEGER NOT NULL,
    distance VARCHAR(100) NOT NULL,
    origin_id INTEGER NOT NULL,
    price FLOAT NOT NULL,
    FOREIGN KEY (origin_id) REFERENCES origins(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (address_id) REFERENCES address(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE destinations (
    id SERIAL PRIMARY KEY,
    address_id INTEGER NOT NULL,
    duration INTEGER NOT NULL,
    distance VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    origin_id INTEGER,
    middle_id INTEGER,
    FOREIGN KEY (address_id) REFERENCES address(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (origin_id) REFERENCES origins(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (middle_id) REFERENCES middles(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE travels (
    id SERIAL PRIMARY KEY,
    status BOOLEAN NOT NULL,
    user_id INTEGER NOT NULL,
    renavam VARCHAR(11) NOT NULL,
    departure TIMESTAMP WITH TIME ZONE NOT NULL,
    origin_id INTEGER NOT NULL,
    middle_id INTEGER,
    destination_id INTEGER NOT NULL,
    arrival TIMESTAMP WITH TIME ZONE NOT NULL,
    involved INTEGER[] CHECK (array_length(involved, 1) <= 4) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (renavam) REFERENCES cars(renavam) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (origin_id) REFERENCES origins(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (middle_id) REFERENCES middles(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE FUNCTION create_origin(
    p_address_id INTEGER,
    p_space INTEGER
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_id INTEGER;
BEGIN
    INSERT INTO origins(address_id, space)
    VALUES(p_address_id, p_space)
    RETURNING id INTO v_id;

    RETURN v_id;
END;
$$;

CREATE FUNCTION create_middle(
    p_address_id INTEGER,
    p_space INTEGER,
    p_duration INTEGER,
    p_distance VARCHAR(100),
    p_origin_id INTEGER
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_id INTEGER;
    p_price FLOAT;
BEGIN
    p_price := 35 + (p_duration / 3600.0) * 10;
    
    INSERT INTO middles(address_id, space, duration, distance, price, origin_id)
    VALUES(p_address_id, p_space, p_duration, p_distance, p_price, p_origin_id)
    RETURNING id INTO v_id;

    RETURN v_id;
END;
$$;

CREATE FUNCTION create_destination(
    p_address_id INTEGER,
    p_duration INTEGER,
    p_distance VARCHAR(100),
    p_origin_id INTEGER,
    p_middle_id INTEGER
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_id INTEGER;
    p_price FLOAT;
BEGIN
    p_price := 35 + (p_duration / 3600.0) * 10;
    
    INSERT INTO destinations(address_id, duration, distance, price, origin_id, middle_id)
    VALUES(p_address_id, p_duration, p_distance, p_price, p_origin_id, p_middle_id)
    RETURNING id INTO v_id;

    RETURN v_id;
END;
$$;

CREATE FUNCTION _create_travel(
    p_origin_address_id INTEGER,
    p_space INTEGER,
    p_middle_address_id INTEGER,
    p_middle_duration INTEGER,
    p_middle_distance VARCHAR(100),
    p_destination_address_id INTEGER,
    p_destination_duration INTEGER,
    p_destination_distance VARCHAR(100)
) RETURNS TABLE(origin_id INTEGER, middle_id INTEGER, destination_id INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    v_origin_id INTEGER;
    v_middle_id INTEGER;
    v_destination_id INTEGER;
BEGIN
    v_origin_id := create_origin(p_origin_address_id, p_space);
    
    IF p_middle_address_id IS NOT NULL THEN
        v_middle_id := create_middle(p_middle_address_id, p_space, p_middle_duration, p_middle_distance, v_origin_id);
    ELSE
        v_middle_id := NULL;
    END IF;

    v_destination_id := create_destination(p_destination_address_id, p_destination_duration, p_destination_distance, v_origin_id, v_middle_id);

    RETURN QUERY SELECT v_origin_id, v_middle_id, v_destination_id;
END;
$$;


CREATE FUNCTION valid_travel(
    p_user_id INTEGER,
    p_departure TIMESTAMP WITH TIME ZONE,
    p_arrival TIMESTAMP WITH TIME ZONE 
) RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    is_valid BOOLEAN := TRUE;
BEGIN
    IF EXISTS (
        SELECT 1
        FROM travels
        WHERE user_id = p_user_id AND status = TRUE
        AND (
            (p_departure < arrival AND p_arrival > departure)
        )
    ) THEN
        is_valid := FALSE;
    END IF;
    RETURN is_valid;
END;
$$;

CREATE FUNCTION create_travel(
    p_user_id INTEGER,
    p_renavam VARCHAR,
    p_space INTEGER,
    p_departure TIMESTAMP WITH TIME ZONE,
    p_origin_address_id INTEGER,
    p_middle_address_id INTEGER,
    p_middle_duration INTEGER,
    p_middle_distance VARCHAR,
    p_destination_address_id INTEGER,
    p_destination_duration INTEGER,
    p_destination_distance VARCHAR
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_origin_id INTEGER;
    v_middle_id INTEGER;
    v_destination_id INTEGER;
    v_id INTEGER;
    v_arrival TIMESTAMP WITH TIME ZONE;
BEGIN
    SELECT origin_id, middle_id, destination_id INTO
        v_origin_id, v_middle_id, v_destination_id
    FROM _create_travel(
        p_origin_address_id,
        p_space,
        p_middle_address_id,
        p_middle_duration,
        p_middle_distance,
        p_destination_address_id,
        p_destination_duration,
        p_destination_distance
    );
    v_arrival := p_departure + ((COALESCE(p_middle_duration, 0) + COALESCE(p_destination_duration, 0)) * INTERVAL '1 second');

    IF valid_travel(p_user_id, p_departure, v_arrival) THEN
        INSERT INTO travels(status, user_id, renavam, departure, origin_id, middle_id, destination_id, arrival, involved)
        VALUES (TRUE, p_user_id, p_renavam, p_departure, v_origin_id, v_middle_id, v_destination_id, v_arrival, '{}')
        RETURNING id INTO v_id;
        RETURN v_id;
    ELSE
        RAISE EXCEPTION 'INVALID TRAVEL';
    END IF;
END;
$$;

CREATE TYPE travel_public AS (
    travel_id INTEGER,
    status BOOLEAN,
    user_id INTEGER,
    renavam VARCHAR,
    departure TIMESTAMP WITH TIME ZONE,
    origin_space INTEGER,
    origin_cep VARCHAR,
    origin_street VARCHAR,
    origin_city VARCHAR,
    origin_state VARCHAR,
    origin_district VARCHAR,
    origin_house_number VARCHAR,
    middle_space INTEGER,
    middle_duration INTEGER,
    middle_distance VARCHAR,
    middle_price FLOAT,
    middle_cep VARCHAR,
    middle_street VARCHAR,
    middle_city VARCHAR,
    middle_state VARCHAR,
    middle_district VARCHAR,
    middle_house_number VARCHAR,
    destination_duration INTEGER,
    destination_distance VARCHAR,
    destination_price FLOAT,
    destination_cep VARCHAR,
    destination_street VARCHAR,
    destination_city VARCHAR,
    destination_state VARCHAR,
    destination_district VARCHAR,
    destination_house_number VARCHAR,
    arrival TIMESTAMP WITH TIME ZONE,
    involved INTEGER[]
);

CREATE FUNCTION get_travel(
    p_id INTEGER
) RETURNS SETOF travel_public
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        t.id,
        t.status,
        t.user_id,
        t.renavam,
        t.departure,
        o.space,
        ao.cep,
        ao.street,
        ao.city,
        ao.state,
        ao.district,
        ao.house_number,
        m.space,
        m.duration,
        m.distance,
        m.price,
        am.cep, 
        am.street,
        am.city,
        am.state,
        am.district,
        am.house_number,
        d.duration,
        d.distance,
        d.price,
        ad.cep,
        ad.street,
        ad.city,
        ad.state,
        ad.district,
        ad.house_number,
        t.arrival,
        t.involved
    FROM travels t
    LEFT JOIN origins o ON t.origin_id = o.id
    LEFT JOIN address ao ON o.address_id = ao.id
    LEFT JOIN middles m ON t.middle_id = m.id
    LEFT JOIN address am ON m.address_id = am.id
    LEFT JOIN destinations d ON t.destination_id = d.id
    LEFT JOIN address ad ON d.address_id = ad.id
    WHERE t.id = p_id;
END;
$$;

CREATE FUNCTION get_travel_by_user(
    p_user_id INTEGER
) RETURNS SETOF travel_public
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        t.id,
        t.status,
        t.user_id,
        t.renavam,
        t.departure,
        o.space,
        ao.cep,
        ao.street,
        ao.city,
        ao.state,
        ao.district,
        ao.house_number,
        m.space,
        m.duration,
        m.distance,
        m.price,
        am.cep, 
        am.street,
        am.city,
        am.state,
        am.district,
        am.house_number,
        d.duration,
        d.distance,
        d.price,
        ad.cep,
        ad.street,
        ad.city,
        ad.state,
        ad.district,
        ad.house_number,
        t.arrival,
        t.involved
    FROM travels t
    LEFT JOIN origins o ON t.origin_id = o.id
    LEFT JOIN address ao ON o.address_id = ao.id
    LEFT JOIN middles m ON t.middle_id = m.id
    LEFT JOIN address am ON m.address_id = am.id
    LEFT JOIN destinations d ON t.destination_id = d.id
    LEFT JOIN address ad ON d.address_id = ad.id
    WHERE t.user_id = p_user_id OR p_user_id = ANY(t.involved);
END;
$$;

CREATE FUNCTION search_travel(
    p_leaving VARCHAR,
    p_going VARCHAR,
    p_day DATE
) RETURNS SETOF travel_public
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        t.id,
        t.status,
        t.user_id,
        t.renavam,
        t.departure,
        o.space,
        ao.cep,
        ao.street,
        ao.city,
        ao.state,
        ao.district,
        ao.house_number,
        m.space,
        m.duration,
        m.distance,
        m.price,
        am.cep, 
        am.street,
        am.city,
        am.state,
        am.district,
        am.house_number,
        d.duration,
        d.distance,
        d.price,
        ad.cep,
        ad.street,
        ad.city,
        ad.state,
        ad.district,
        ad.house_number,
        t.arrival,
        t.involved
    FROM travels AS t
    LEFT JOIN origins o ON t.origin_id = o.id
    LEFT JOIN address ao ON o.address_id = ao.id
    LEFT JOIN middles m ON t.middle_id = m.id
    LEFT JOIN address am ON m.address_id = am.id
    LEFT JOIN destinations d ON t.destination_id = d.id
    LEFT JOIN address ad ON d.address_id = ad.id
    WHERE 
      t.departure::DATE = p_day
      AND t.status = TRUE 
      AND COALESCE(array_length(t.involved, 1), 0) < 4
      AND (
        (ao.city = p_leaving OR am.city = p_leaving) 
        AND (ad.city = p_going OR am.city = p_going)
        AND NOT (am.city = p_leaving AND am.city = p_going)
      );
END;
$$;


CREATE FUNCTION valid_confirm_travel(
    p_user_id INTEGER,
    p_travel_id INTEGER
) RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    is_valid BOOLEAN := TRUE;
    rec RECORD;
BEGIN
    FOR rec IN
        SELECT arrival, departure 
        FROM get_travel_by_user(p_user_id)
    LOOP
        IF EXISTS (
            SELECT 1
            FROM travels AS t
            WHERE t.user_id = p_user_id 
            OR p_user_id = ANY(t.involved)
            OR (rec.departure < t.arrival AND rec.arrival > t.departure)
        ) THEN
            is_valid := FALSE;
            EXIT;
        END IF;
    END LOOP;

    RETURN is_valid;
END;
$$;

CREATE FUNCTION confirm_travel(
    p_user_id INTEGER,
    p_travel_id INTEGER
) RETURNS VOID 
LANGUAGE plpgsql
AS $$
BEGIN
    IF valid_confirm_travel(p_user_id, p_travel_id) THEN
        UPDATE travels
        SET involved = array_append(involved, p_user_id)
        WHERE id = p_travel_id;
    ELSE
        RAISE EXCEPTION 'Invalid confirm travel';
    END IF;
END;
$$;


-----------------------------------------------------------------
---------------------------AVALIACAO-------------------------------
-----------------------------------------------------------------

--criacao da tabela de avaliacao
CREATE TYPE rating_type AS ENUM ('CARONISTA', 'CARONEIRO');
CREATE TYPE rating_grade AS ENUM ('PESSIMO', 'RUIM', 'MEDIANO', 'BOM', 'OTIMO');
CREATE TABLE Rate (
    id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL,
    recipient_id INTEGER NOT NULL,
    creation TIMESTAMP NOT NULL,
    rate_type rating_type NOT NULL,
    grade rating_grade NOT NULL,
    content VARCHAR(255),
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT unique_author_recipient_rate_type UNIQUE (author_id, recipient_id, rate_type)  -- Restrições de unicidade
);


--função para criar uma avaliacao nova
CREATE FUNCTION create_or_update_rating(
    p_author_id INTEGER,
    p_recipient_id INTEGER,
    p_rate_type rating_type,
    p_grade rating_grade,
    p_content VARCHAR(255)
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_rating_id INTEGER;
BEGIN
    -- Verifica se já existe uma avaliação com os parâmetros fornecidos
    SELECT id INTO v_rating_id
    FROM Rate
    WHERE author_id = p_author_id
    AND recipient_id = p_recipient_id
    AND rate_type = p_rate_type;

    -- Se a avaliação já existir, atualiza a existente
    IF v_rating_id IS NOT NULL THEN
        UPDATE Rate
        SET grade = p_grade,
            content = p_content,
            creation = NOW()
        WHERE id = v_rating_id;
    ELSE
        -- Se não existir, insere uma nova avaliação
        INSERT INTO Rate (author_id, recipient_id, creation, rate_type, grade, content)
        VALUES (p_author_id, p_recipient_id, NOW(), p_rate_type, p_grade, p_content)
        RETURNING id INTO v_rating_id;
    END IF;

    -- Retorna o ID da avaliação, seja nova ou atualizada
    RETURN v_rating_id;
END;
$$;


CREATE OR REPLACE FUNCTION get_rating_by_id(
    p_id INTEGER
)
RETURNS TABLE (
    id INTEGER,
    author_id INTEGER,
    recipient_id INTEGER,
    rate_type rating_type,
    grade rating_grade,
    content VARCHAR,
    creation TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.id, 
        r.author_id, 
        r.recipient_id, 
        r.rate_type, 
        r.grade, 
        r.content, 
        r.creation
    FROM Rate r
    WHERE r.id = p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_rates_by_user(p_user_id INTEGER)
RETURNS TABLE (
    id INTEGER,
    author_id INTEGER,
    recipient_id INTEGER,
    rate_type rating_type,
    grade rating_grade,
    content VARCHAR,
    creation TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.id, 
        r.author_id, 
        r.recipient_id, 
        r.rate_type, 
        r.grade, 
        r.content, 
        r.creation
    FROM Rate r
    WHERE r.recipient_id = p_user_id
    ORDER BY r.rate_type;
END;
$$;

CREATE OR REPLACE FUNCTION check_rating_exists(
    p_author_id INTEGER,
    p_recipient_id INTEGER,
    p_rate_type rating_type
)
RETURNS TABLE (
    id INTEGER,
    author_id INTEGER,
    recipient_id INTEGER,
    rate_type rating_type,
    grade rating_grade,
    content VARCHAR,
    creation TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.id, 
        r.author_id, 
        r.recipient_id, 
        r.rate_type, 
        r.grade, 
        r.content, 
        r.creation
    FROM Rate r
    WHERE r.author_id = p_author_id
      AND r.recipient_id = p_recipient_id
      AND r.rate_type = p_rate_type;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_rating()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Se o rating_type for 'CARONISTA', atualiza a nota média do motorista (tabela drivers)
    IF NEW.rate_type = 'CARONISTA' THEN
        UPDATE drivers
        SET rating = (
            SELECT AVG(
                CASE 
                    WHEN grade = 'OTIMO' THEN 5
                    WHEN grade = 'BOM' THEN 4
                    WHEN grade = 'MEDIANO' THEN 3
                    WHEN grade = 'RUIM' THEN 2
                    WHEN grade = 'PESSIMO' THEN 1
                END
            )
            FROM Rate
            WHERE recipient_id = NEW.recipient_id
            AND rate_type = 'CARONISTA'
        )
        WHERE user_id = NEW.recipient_id;

    -- Se o rating_type for 'CARONEIRO', atualiza a nota média do passageiro (tabela users)
    ELSIF NEW.rate_type = 'CARONEIRO' THEN
        UPDATE users
        SET passenger_rating = (
            SELECT AVG(
                CASE 
                    WHEN grade = 'OTIMO' THEN 5
                    WHEN grade = 'BOM' THEN 4
                    WHEN grade = 'MEDIANO' THEN 3
                    WHEN grade = 'RUIM' THEN 2
                    WHEN grade = 'PESSIMO' THEN 1
                END
            )
            FROM Rate
            WHERE recipient_id = NEW.recipient_id
            AND rate_type = 'CARONEIRO'
        )
        WHERE id = NEW.recipient_id;
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_update_rating
AFTER INSERT OR UPDATE ON Rate
FOR EACH ROW
EXECUTE FUNCTION update_rating();

-----------------------------------------------------------------
---------------------------CHAT----------------------------------
-----------------------------------------------------------------

CREATE TABLE chats(
    id SERIAL PRIMARY KEY NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    first INTEGER NOT NULL,
    second INTEGER NOT NULL,
    FOREIGN KEY (first) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (second) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE messages(
    id SERIAL PRIMARY KEY NOT NULL,
    chat_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    content VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE FUNCTION create_chat(
    p_first INTEGER,
    p_second INTEGER
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO chats(first, second)
    VALUES (p_first, p_second);
END;
$$;


CREATE FUNCTION get_chats(
    p_user_id INTEGER
)
RETURNS TABLE(
    id INTEGER,
    first VARCHAR,
    second VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id,
           CASE 
               WHEN c.first = p_user_id THEN uf.name
               ELSE us.name
           END AS first,
           CASE 
               WHEN c.first = p_user_id THEN us.name
               ELSE uf.name
           END AS second
    FROM chats AS c
    LEFT JOIN users AS uf ON c.first = uf.id
    LEFT JOIN users AS us ON c.second = us.id
    WHERE c.first = p_user_id OR c.second = p_user_id;
END;
$$;


CREATE FUNCTION get_chat(
    p_first INTEGER,
    p_second INTEGER
)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE 
    v_id INTEGER;
BEGIN
    SELECT id INTO v_id 
    FROM chats 
    WHERE (p_first = first OR p_first = second) 
    AND (p_second = first OR p_second = second);
    
    RETURN v_id;
END;
$$;


CREATE FUNCTION get_messages(
    p_chat_id INTEGER
)
RETURNS TABLE(
    sender VARCHAR,
    content VARCHAR,
    created_at TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT u.name, m.content, m.created_at
    FROM messages m 
    LEFT JOIN users u ON m.sender_id = u.id 
    WHERE m.chat_id = p_chat_id;
END;
$$;

CREATE FUNCTION get_users_from_chat(
    p_chat_id INTEGER,
    p_user_id INTEGER
)
RETURNS TABLE(
    first_name VARCHAR,
    second_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        CASE 
            WHEN c.first = p_user_id THEN uf.name
            ELSE us.name
        END AS first_name,
        CASE 
            WHEN c.first = p_user_id THEN us.name
            ELSE uf.name
        END AS second_name
    FROM chats c
    LEFT JOIN users uf ON c.first = uf.id 
    LEFT JOIN users us ON c.second = us.id 
    WHERE c.id = p_chat_id;
END;
$$;


CREATE FUNCTION save_message(
    p_chat_id INTEGER,
    p_sender_id INTEGER,
    p_content VARCHAR
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO messages (chat_id, sender_id, content)
    VALUES(p_chat_id, p_sender_id, p_content);
END;
$$;
