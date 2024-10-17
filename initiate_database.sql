CREATE TABLE admins
(
    admin_username VARCHAR,
    admin_id       INT,
    lang_code      VARCHAR
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
    lang_code          VARCHAR,
    account_balance    NUMERIC(9, 2)
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
    location           NUMERIC(9, 6)[],
    account_balance    NUMERIC(9, 2)
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
    restaurant_id     INT,
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
    order_open_date   TIMESTAMP,
    order_close_date  TIMESTAMP,
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

-- CREATE TRIGGER order_status_change_trigger
--     AFTER INSERT OR UPDATE OF order_status
--     ON orders
--     FOR EACH ROW
-- EXECUTE PROCEDURE notify_order_status_change();
--
--
-- CREATE OR REPLACE FUNCTION notify_order_status_change()
--     RETURNS TRIGGER AS
-- $$
-- DECLARE
--     payload JSON;
-- BEGIN
--     payload := json_build_object(
--         'order_uuid', NEW.order_uuid,
--         'new_status', NEW.order_status,
--         'rest_uuid', NEW.restaurant_uuid,
--         'customer_id', NEW.customer_id,
--         'courier_id', NEW.courier_id
--     );
--     PERFORM pg_notify('order_status_channel', payload);
-- END;
-- $$ LANGUAGE plpgsql;
