CREATE TABLE admins (
    admin_username VARCHAR,
    admin_id INT
);
CREATE TABLE couriers (
    courier_id INT,
    courier_username VARCHAR,
    courier_legal_name VARCHAR,
    courier_type VARCHAR,
    courier_status VARCHAR,
    courier_rating NUMERIC(3, 2),
    courier_phone_num VARCHAR
);
CREATE TABLE customers (
    customer_id INT,
    customer_username VARCHAR,
    customer_name VARCHAR,
    customer_location NUMERIC(9, 6) [],
    customer_phone_num VARCHAR
);
CREATE TABLE restaurants (
    restaurant_uuid uuid,
    restaurant_tg_ids INT [],
    restaurant_name VARCHAR,
    restaurant_type VARCHAR,
    restaurant_is_open BOOLEAN
);
CREATE TABLE dishes (
    restaurant_uuid uuid,
    dish_uuid uuid,
    category VARCHAR,
    dish_name VARCHAR,
    dish_price NUMERIC(6, 2),
    dish_is_available BOOLEAN
);
CREATE TABLE orders (
    order_uuid uuid,
    restaurant_uuid uuid,
    restaurant_name VARCHAR,
    courier_id INT,
    courier_name VARCHAR,
    customer_id INT,
    customer_name VARCHAR,
    delivery_location NUMERIC(9, 6) [],
    dishes VARCHAR [],
    dishes_price NUMERIC(6, 2),
    courier_fee NUMERIC(6, 2),
    service_fee NUMERIC(6, 2),
    total NUMERIC(6, 2),
    order_date TIMESTAMP,
    order_status VARCHAR
);
CREATE TABLE cart (
    customer_id INT,
    dishes VARCHAR [],
    price NUMERIC(6, 2)
);
CREATE EXTENSION "pgcrypto";