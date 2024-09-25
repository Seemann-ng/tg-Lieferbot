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
    courier_rating FLOAT(2),
    courier_phone_num VARCHAR
);
CREATE TABLE customers (
    customer_id INT,
    customer_name VARCHAR,
    customer_address VARCHAR,
    customer_phone_num VARCHAR
);
CREATE TABLE restaurants (
    restaurant_uuid uuid,
    restaurant_tg_ids INT [],
    restaurant_name VARCHAR,
    restaurant_is_open BOOLEAN
);
CREATE TABLE dishes (
    restaurant_uuid uuid,
    category VARCHAR,
    dish_name VARCHAR,
    dish_price FLOAT(2),
    dish_is_available BOOLEAN
);
CREATE TABLE orders (
    order_uuid uuid,
    restaurant_name VARCHAR,
    restaurant_uuid uuid,
    courier_name VARCHAR,
    courier_id INT,
    customer_name VARCHAR,
    customer_id INT,
    delivery_address VARCHAR,
    dishes VARCHAR [],
    dishes_price FLOAT(2),
    courier_fee FLOAT(2),
    service_fee FLOAT(2),
    total FLOAT(2),
    order_status VARCHAR
);
CREATE EXTENSION "pgcrypto";