CREATE TABLE admins
(
    admin_username VARCHAR NOT NULL,
    admin_id       BIGINT  NOT NULL PRIMARY KEY,
    lang_code      VARCHAR NOT NULL DEFAULT 'en_US'
);


CREATE TABLE couriers
(
    courier_id         BIGINT         NOT NULL PRIMARY KEY,
    courier_username   VARCHAR        NOT NULL,
    courier_legal_name VARCHAR        NOT NULL,
    courier_type       VARCHAR        NOT NULL DEFAULT '0',
    courier_status     BOOLEAN        NOT NULL DEFAULT FALSE,
    is_occupied        BOOLEAN        NOT NULL DEFAULT FALSE,
    courier_rating     NUMERIC(3, 2)  NOT NULL DEFAULT 5.00,
    courier_phone_num  VARCHAR        NOT NULL,
    lang_code          VARCHAR        NOT NULL DEFAULT 'en_US',
    account_balance    NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    paypal_id          VARCHAR        NOT NULL
);


CREATE TABLE customers
(
    customer_id        BIGINT          NOT NULL PRIMARY KEY,
    customer_username  VARCHAR         NOT NULL,
    customer_name      VARCHAR         NOT NULL,
    customer_location  NUMERIC(9, 6)[] NOT NULL,
    customer_phone_num VARCHAR         NOT NULL DEFAULT '',
    lang_code          VARCHAR         NOT NULL DEFAULT 'en_US'
);


CREATE TABLE restaurants
(
    restaurant_uuid    uuid            NOT NULL PRIMARY KEY,
    restaurant_tg_id   BIGINT          NOT NULL,
    restaurant_name    VARCHAR         NOT NULL,
    restaurant_type    VARCHAR         NOT NULL,
    restaurant_is_open BOOLEAN         NOT NULL,
    lang_code          VARCHAR         NOT NULL DEFAULT 'en_US',
    address            VARCHAR         NOT NULL,
    location           NUMERIC(9, 6)[] NOT NULL,
    paypal_id          VARCHAR         NOT NULL
);


CREATE TABLE dishes
(
    restaurant_uuid   uuid           NOT NULL primary key,
    dish_uuid         uuid           NOT NULL,
    category          VARCHAR        NOT NULL DEFAULT 'No category',
    dish_name         VARCHAR        NOT NULL,
    dish_description  VARCHAR        NOT NULL,
    dish_price        NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    dish_is_available BOOLEAN        NOT NULL DEFAULT TRUE
);


CREATE TABLE orders
(
    order_uuid        uuid            NOT NULL PRIMARY KEY,
    restaurant_uuid   uuid            NOT NULL,
    restaurant_id     BIGINT          NOT NULL,
    restaurant_name   VARCHAR         NOT NULL,
    courier_id        BIGINT          NOT NULL DEFAULT -1,
    courier_name      VARCHAR         NOT NULL,
    customer_id       BIGINT          NOT NULL,
    customer_name     VARCHAR         NOT NULL,
    delivery_location NUMERIC(9, 6)[] NOT NULL,
    delivery_distance NUMERIC(7, 2)   NOT NULL DEFAULT 0.00,
    dishes            VARCHAR[]       NOT NULL,
    dishes_subtotal   NUMERIC(10, 2)  NOT NULL,
    courier_fee       NUMERIC(10, 2)  NOT NULL,
    service_fee       NUMERIC(10, 2)  NOT NULL,
    total             NUMERIC(10, 2)  NOT NULL,
    order_comment     VARCHAR         NOT NULL DEFAULT '',
    order_open_date   TIMESTAMP       NOT NULL,
    order_close_date  TIMESTAMP,
    order_status      VARCHAR         NOT NULL,
    paypal_order_id   VARCHAR         NOT NULL
);


CREATE TABLE cart
(
    customer_id     BIGINT         NOT NULL PRIMARY KEY,
    restaurant_type VARCHAR        NOT NULL,
    restaurant_uuid uuid           NOT NULL,
    dishes_uuids    VARCHAR[]      NOT NULL,
    subtotal        NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    service_fee     NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    courier_fee     NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    total           NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    order_comment   VARCHAR        NOT NULL DEFAULT ''
);


CREATE EXTENSION "pgcrypto";
