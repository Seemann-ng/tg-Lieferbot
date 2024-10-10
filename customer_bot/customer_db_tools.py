from typing import Dict, List, Tuple, Any

import psycopg2
import telebot.types as types
from environs import Env

from tools.cursor_tool import cursor
from tools.logger_tool import logger, logger_decorator

env = Env()
env.read_env()

DEF_LANG = env.str("DEF_LANG", default="en_US")


class Interface:
    def __init__(self, data_to_read: types.Message | types.CallbackQuery):
        self.data_to_read = data_to_read
        logger.info(f"Interface instance initialized with {type(self.data_to_read)}.")

    @cursor
    @logger_decorator
    def user_in_db(self, curs: psycopg2.extensions.cursor) -> str | None:
        """Check if Customer is in the DB and if so get their name or Telegram username.

        Args:
            curs: PostgreSQL cursor object.

        Returns:
            Customer name from the DB if Customer is in the DB and has provided their name,
            Telegram username if Customer is in the DB and has NOT provided their name.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("SELECT customer_name, customer_username "
                    "FROM customers "
                    "WHERE customers.customer_id = %s",
                    (customer_id,))
        if customer_names := curs.fetchone():
            if customer_names[0]:
                return customer_names[0]
            return customer_names[1]

    @cursor
    @logger_decorator
    def add_customer(self, curs: psycopg2.extensions.cursor) -> None:
        """Add Customer to DB.

        Args:
            curs: PostgreSQL cursor object.

        """
        if not self.user_in_db():
            customer_id = self.data_to_read.from_user.id
            customer_username = self.data_to_read.from_user.username
            curs.execute("INSERT INTO customers (customer_id, customer_username) "
                        "VALUES (%s, %s)",
                        (customer_id, customer_username))

    @cursor
    @logger_decorator
    def update_name(self, curs: psycopg2.extensions.cursor) -> None:
        """Update Customer name in the DB.

        Args:
            curs: PostgreSQL cursor object.

        """
        customer_name = self.data_to_read.text
        customer_id = self.data_to_read.from_user.id
        curs.execute("UPDATE customers "
                    "SET customer_name = %s "
                    "WHERE customers.customer_id = %s",
                    (customer_name, customer_id))

    @cursor
    @logger_decorator
    def update_phone_number(self, phone_number: str, curs: psycopg2.extensions.cursor) -> None:
        """Update Customer phone number in the DB.

        Args:
            phone_number: Customer's phone number.
            curs: PostgreSQL cursor object.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("UPDATE customers "
                    "SET customer_phone_num = %s "
                    "WHERE customers.customer_id = %s",
                    (phone_number, customer_id))

    @cursor
    @logger_decorator
    def update_customer_location(self, curs: psycopg2.extensions.cursor) -> None:
        """Update Customer Location in the DB.

        Args:
            curs: PostgreSQL cursor object.

        """
        latitude = self.data_to_read.location.latitude
        longitude = self.data_to_read.location.longitude
        customer_id = self.data_to_read.from_user.id
        curs.execute("UPDATE customers "
                    "SET customer_location = '{%s, %s}' "
                    "WHERE customers.customer_id = %s",
                    (latitude, longitude, customer_id))

    @cursor
    @logger_decorator
    def delete_customer(self, curs: psycopg2.extensions.cursor) -> None:
        """Delete Customer from the DB.

        Args:
            curs: PostgreSQL cursor object.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("DELETE FROM customers WHERE customers.customer_id = %s", (customer_id,))

    @cursor
    @logger_decorator
    def show_my_orders(self, curs: psycopg2.extensions.cursor) -> List[Tuple[Any, ...]] | None:
        """Get list of Customer's orders.

        Args:
            curs: PostgreSQL cursor object.

        Returns:
            List of tuples with Customer's orders info inside them.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("SELECT order_uuid, restaurant_name, courier_name, dishes, total, order_date, order_status "
                    "FROM orders "
                    "WHERE orders.customer_id = %s",
                    (customer_id,))
        orders = curs.fetchall()
        return orders

    @staticmethod
    @cursor
    @logger_decorator
    def show_restaurant_types(curs: psycopg2.extensions.cursor) -> List[Tuple[Any, ...]] | None:
        """Get list of restaurant types containing at least one restaurant which is open now in each of the types.

        Args:
            curs: PostgreSQL cursor object.

        Returns:
            List of available restaurant types.

        """
        curs.execute("SELECT DISTINCT restaurant_type "
                    "FROM restaurants "
                    "WHERE restaurants.restaurant_is_open=TRUE "
                    "ORDER BY restaurant_type")
        restaurant_types = curs.fetchall()
        return restaurant_types

    @cursor
    @logger_decorator
    def show_restaurants(self, curs: psycopg2.extensions.cursor) -> List[Tuple[Any, ...]] | None:
        """Get list of open restaurants in chosen restaurant type.

        Args:
            curs: PostgreSQL cursor object.

        Returns:
            List of available restaurants.

        """
        callback_data = self.data_to_read.data
        curs.execute("SELECT restaurant_name, restaurant_uuid "
                    "FROM restaurants "
                    "WHERE restaurants.restaurant_type = %s "
                    "AND restaurants.restaurant_is_open = TRUE",
                    (callback_data,))
        restaurants = curs.fetchall()
        return restaurants

    @cursor
    @logger_decorator
    def show_dish_categories(self, curs: psycopg2.extensions.cursor) -> List[Tuple[Any, ...]] | None:
        """Get list of available dish categories in the chosen restaurant.

        Args:
            curs: PostgreSQL cursor object.

        Returns:
            List of available dish categories.

        """
        callback_data = self.data_to_read.data
        curs.execute("SELECT DISTINCT category "
                    "FROM dishes "
                    "WHERE dishes.restaurant_uuid = %s "
                    "AND dishes.dish_is_available = TRUE",
                    (callback_data,))
        categories = curs.fetchall()
        return categories

    @cursor
    @logger_decorator
    def show_dishes(self, curs: psycopg2.extensions.cursor) -> List[Tuple[Any, ...]]:
        """Get list of available dishes in specified category and restaurant.

        Args:
            curs: PostgreSQL cursor object.

        Returns:
            List of available dishes.

        """
        restaurant_uuid = self.get_from_cart("restaurant_uuid")
        callback_data = self.data_to_read.data
        curs.execute("SELECT dish_name, dish_uuid "
                    "FROM dishes "
                    "WHERE dishes.restaurant_uuid = %s "
                    "AND dishes.dish_is_available = TRUE "
                    "AND dishes.category = %s",
                    (restaurant_uuid, callback_data))
        dishes = curs.fetchall()
        return dishes

    @cursor
    @logger_decorator
    def rest_name_by_uuid(self, curs: psycopg2.extensions.cursor) -> str | None:
        """Get restaurant name by its UUID.

        Args:
            curs: PostgreSQL cursor object.

        Returns:
            Restaurant name.

        """
        callback_data = self.data_to_read.data
        curs.execute("SELECT restaurant_name "
                    "FROM restaurants "
                    "WHERE restaurants.restaurant_uuid = %s",
                    (callback_data,))
        rest_name = curs.fetchone()
        return rest_name[0]

    @cursor
    @logger_decorator
    def get_dish(self, curs: psycopg2.extensions.cursor) -> Tuple[Any, ...] | None:
        """Get dish info (name, description and price) by given dish UUID.

        Args:
            curs: PostgreSQL cursor object.

        Returns:
            Tuple with dish info.

        """
        callback_data = self.data_to_read.data
        curs.execute("SELECT dish_name, dish_description, dish_price "
                    "FROM dishes "
                    "WHERE dishes.dish_uuid = %s",
                    (callback_data,))
        dish = curs.fetchone()
        return dish

    @cursor
    @logger_decorator
    def new_cart(self, curs: psycopg2.extensions.cursor) -> None:
        """Create new cart in the DB.cart table and add Customer's Telegram ID in it.

        Args:
            curs: PostgreSQL cursor object.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("INSERT INTO cart (customer_id) VALUES (%s)", (customer_id,))

    @cursor
    @logger_decorator
    def add_to_cart(self, column_name: str, curs: psycopg2.extensions.cursor) -> None:
        """Add required info into cart.

        Args:
            column_name: Name of column containing required info.
            curs: PostgreSQL cursor object.

        """
        callback_data = self.data_to_read.data
        customer_id = self.data_to_read.from_user.id
        curs.execute("UPDATE cart "
                    "SET " + column_name + " =%s "
                    "WHERE cart.customer_id = %s",
                    (callback_data, customer_id))

    @cursor
    @logger_decorator
    def get_from_cart(self, column_name: str, curs: psycopg2.extensions.cursor) -> float | int | str | List[Any] | None:
        """Get required info from cart.

        Args:
            column_name: Name of column containing required info.
            curs: PostgreSQL cursor object.

        Returns:
            Required info.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("SELECT " + column_name + " FROM cart WHERE cart.customer_id = %s", (customer_id,))
        value = curs.fetchone()
        return value[0] if value is not None else None

    @cursor
    @logger_decorator
    def delete_from_cart(self, column_name: str, curs: psycopg2.extensions.cursor) -> None:
        """Delete required info from cart.

        Args:
            column_name: Name of column containing required info.
            curs: PostgreSQL cursor object.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("UPDATE cart SET " + column_name + " =null WHERE cart.customer_id = %s", (customer_id,))

    @cursor
    @logger_decorator
    def delete_cart(self, curs: psycopg2.extensions.cursor) -> None:
        """Delete cart connected to given Customer's Telegram ID.

        Args:
            curs: PostgreSQL cursor object.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("DELETE FROM cart WHERE cart.customer_id = %s", (customer_id,))

    @cursor
    @logger_decorator
    def check_if_location(self, curs: psycopg2.extensions.cursor) -> Dict[str, float] | None:
        """Check if Customer's location is provided and return it if so.

        Args:
            curs: PostgreSQL cursor object.

        Returns:
            Customer's longitude and latitude if ones are provided.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("SELECT customer_location "
                    "FROM customers "
                    "WHERE customers.customer_id = %s",
                    (customer_id,))
        if latlon := curs.fetchone()[0]:
            location = {"lat": latlon[0], "lon": latlon[1]}
            return location

    @cursor
    @logger_decorator
    def get_customer_lang(self, curs: psycopg2.extensions.cursor) -> str:
        """Get code of Customer's chosen language.

        Args:
            curs: PostgreSQL cursor object.

        Returns:
            Code of Customer's chosen language
            if Customer has chosen one,
            otherwise default language code, set in .env.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("SELECT lang_code FROM customers WHERE customers.customer_id = %s", (customer_id,))
        if customer_lang := curs.fetchone():
            if customer_lang := customer_lang[0]:
                return customer_lang
        return DEF_LANG


    @cursor
    @logger_decorator
    def set_customer_lang(self, curs: psycopg2.extensions.cursor) -> None:
        """Set language code for Customer.

        Args:
            curs: PostgreSQL cursor object.

        """
        customer_id = self.data_to_read.from_user.id
        lang_code = self.data_to_read.data
        curs.execute("UPDATE customers SET lang_code = %s WHERE customers.customer_id = %s",
                     (lang_code, customer_id))