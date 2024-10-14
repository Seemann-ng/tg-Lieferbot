CREATE TABLE admins
(
    admin_username VARCHAR,
    admin_id       INT
);


CREATE TABLE couriers
(
    courier_id         INT,
    courier_username   VARCHAR,
    courier_legal_name VARCHAR,
    courier_type       VARCHAR,
    courier_status     BOOLEAN,
    is_occupied        BOOLEAN,
    courier_rating     NUMERIC(3, 2),
    courier_phone_num  VARCHAR,
    lang_code          VARCHAR
);


CREATE TABLE customers
(
    customer_id        INT,
    customer_username  VARCHAR,
    customer_name      VARCHAR,
    customer_location  NUMERIC(9, 6)[],
    customer_phone_num VARCHAR,
    lang_code          VARCHAR
);


CREATE TABLE restaurants
(
    restaurant_uuid    uuid,
    restaurant_tg_id   INT,
    restaurant_name    VARCHAR,
    restaurant_type    VARCHAR,
    restaurant_is_open BOOLEAN,
    lang_code          VARCHAR,
    address            VARCHAR,
    location           NUMERIC(9, 6)[]
);


CREATE TABLE dishes
(
    restaurant_uuid   uuid,
    dish_uuid         uuid,
    category          VARCHAR,
    dish_name         VARCHAR,
    dish_description  VARCHAR,
    dish_price        NUMERIC(6, 2),
    dish_is_available BOOLEAN
);


CREATE TABLE orders
(
    order_uuid        uuid,
    restaurant_uuid   uuid,
    restaurant_name   VARCHAR,
    courier_id        INT,
    courier_name      VARCHAR,
    customer_id       INT,
    customer_name     VARCHAR,
    delivery_location NUMERIC(9, 6)[],
    dishes            VARCHAR[],
    dishes_subtotal   NUMERIC(10, 2),
    courier_fee       NUMERIC(10, 2),
    service_fee       NUMERIC(10, 2),
    total             NUMERIC(10, 2),
    order_date        TIMESTAMP,
    order_status      VARCHAR
);


CREATE TABLE cart
(
    customer_id     INT,
    restaurant_type VARCHAR,
    restaurant_uuid uuid,
    dishes_uuids    uuid[],
    subtotal        NUMERIC(10, 2),
    service_fee     NUMERIC(10, 2),
    courier_fee     NUMERIC(10, 2),
    total           NUMERIC(10, 2)
);


CREATE EXTENSION "pgcrypto";
CREATE TRIGGER order_status_change_trigger
    AFTER INSERT OR UPDATE OF order_status
    ON orders
    FOR EACH ROW
EXECUTE PROCEDURE notify_order_status_change();


CREATE OR REPLACE FUNCTION notify_order_status_change()
    RETURNS TRIGGER AS
$$
BEGIN
    PERFORM pg_notify('order_status_channel', NEW.order_uuid::text || ' ' || NEW.order_status::text);
    RETURN NEW;
END;
$$
    LANGUAGE plpgsql;