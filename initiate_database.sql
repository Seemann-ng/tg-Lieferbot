CREATE TABLE admins
(
    admin_username VARCHAR,
    admin_id       INT,
    lang_code      VARCHAR DEFAULT 'en_US'
);


CREATE TABLE couriers
(
    courier_id         INT,
    courier_username   VARCHAR,
    courier_legal_name VARCHAR,
    courier_type       VARCHAR        DEFAULT '0',
    courier_status     BOOLEAN        DEFAULT FALSE,
    is_occupied        BOOLEAN        DEFAULT FALSE,
    courier_rating     NUMERIC(3, 2)  DEFAULT 5.00,
    courier_phone_num  VARCHAR,
    lang_code          VARCHAR        DEFAULT 'en_US',
    account_balance    NUMERIC(10, 2) DEFAULT 0.00,
    paypal_id          VARCHAR
);


CREATE TABLE customers
(
    customer_id        INT,
    customer_username  VARCHAR,
    customer_name      VARCHAR,
    customer_location  NUMERIC(9, 6)[],
    customer_phone_num VARCHAR DEFAULT '',
    lang_code          VARCHAR DEFAULT 'en_US'
);


CREATE TABLE restaurants
(
    restaurant_uuid    uuid,
    restaurant_tg_id   INT,
    restaurant_name    VARCHAR,
    restaurant_type    VARCHAR,
    restaurant_is_open BOOLEAN,
    lang_code          VARCHAR DEFAULT 'en_US',
    address            VARCHAR,
    location           NUMERIC(9, 6)[],
    paypal_id          VARCHAR
);


CREATE TABLE dishes
(
    restaurant_uuid   uuid,
    dish_uuid         uuid,
    category          VARCHAR        DEFAULT 'No category',
    dish_name         VARCHAR,
    dish_description  VARCHAR,
    dish_price        NUMERIC(10, 2) DEFAULT 0.00,
    dish_is_available BOOLEAN        DEFAULT TRUE
);


CREATE TABLE orders
(
    order_uuid        uuid,
    restaurant_uuid   uuid,
    restaurant_id     INT,
    restaurant_name   VARCHAR,
    courier_id        INT           DEFAULT -1,
    courier_name      VARCHAR,
    customer_id       INT,
    customer_name     VARCHAR,
    delivery_location NUMERIC(9, 6)[],
    delivery_distance NUMERIC(7, 2) DEFAULT 0.00,
    dishes            VARCHAR[],
    dishes_subtotal   NUMERIC(10, 2),
    courier_fee       NUMERIC(10, 2),
    service_fee       NUMERIC(10, 2),
    total             NUMERIC(10, 2),
    order_comment     VARCHAR       DEFAULT '',
    order_open_date   TIMESTAMP,
    order_close_date  TIMESTAMP,
    order_status      VARCHAR,
    paypal_order_id   VARCHAR
);


CREATE TABLE cart
(
    customer_id     INT,
    restaurant_type VARCHAR,
    restaurant_uuid uuid,
    dishes_uuids    VARCHAR[],
    subtotal        NUMERIC(10, 2) DEFAULT 0.00,
    service_fee     NUMERIC(10, 2) DEFAULT 0.00,
    courier_fee     NUMERIC(10, 2) DEFAULT 0.00,
    total           NUMERIC(10, 2) DEFAULT 0.00,
    order_comment   VARCHAR        DEFAULT ''
);


CREATE EXTENSION "pgcrypto";
