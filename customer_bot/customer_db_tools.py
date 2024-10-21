import uuid
import random
import datetime
from typing import Any, Dict, List, Tuple

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
            curs: Cursor object from psycopg2 module.

        Returns:
            Customer name from the DB if Customer is in the DB and has provided their name,
            Telegram username if Customer is in the DB and has NOT provided their name.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("SELECT customer_name, customer_username FROM customers WHERE customer_id = %s",
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
            curs: Cursor object from psycopg2 module.

        """
        if not self.user_in_db():
            customer_id = self.data_to_read.from_user.id
            customer_username = self.data_to_read.from_user.username
            curs.execute("INSERT INTO customers (customer_id, customer_username) VALUES (%s, %s)",
                         (customer_id, customer_username))

    @cursor
    @logger_decorator
    def update_name(self, curs: psycopg2.extensions.cursor) -> None:
        """Update Customer name in the DB.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        customer_name = self.data_to_read.text
        customer_id = self.data_to_read.from_user.id
        curs.execute("UPDATE customers SET customer_name = %s WHERE customer_id = %s",
                     (customer_name, customer_id))

    @cursor
    @logger_decorator
    def update_phone_number(self, phone_number: str, curs: psycopg2.extensions.cursor) -> None:
        """Update Customer phone number in the DB.

        Args:
            phone_number: Customer's phone number.
            curs: Cursor object from psycopg2 module.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("UPDATE customers SET customer_phone_num = %s WHERE customer_id = %s",
                     (phone_number, customer_id))

    @cursor
    @logger_decorator
    def update_customer_location(self, curs: psycopg2.extensions.cursor) -> None:
        """Update Customer Location in the DB.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        latitude = self.data_to_read.location.latitude
        longitude = self.data_to_read.location.longitude
        customer_id = self.data_to_read.from_user.id
        curs.execute("UPDATE customers SET customer_location = '{%s, %s}' WHERE customer_id = %s",
                     (latitude, longitude, customer_id))

    @cursor
    @logger_decorator
    def delete_customer(self, curs: psycopg2.extensions.cursor) -> None:
        """Delete Customer from the DB.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))

    @cursor
    @logger_decorator
    def show_my_orders(self, curs: psycopg2.extensions.cursor) -> List[Tuple[Any, ...]]:
        """Get list of Customer's orders.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            List of tuples with Customer's orders info inside them.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("SELECT order_uuid, restaurant_name, courier_name, dishes, total, order_open_date, "
                     "order_status, order_close_date FROM orders WHERE customer_id = %s",
                     (customer_id,))
        orders = curs.fetchall()
        return orders if orders else []

    @staticmethod
    @cursor
    @logger_decorator
    def show_restaurant_types(curs: psycopg2.extensions.cursor) -> List[Tuple[Any, ...]]:
        """Get list of restaurant types containing at least one restaurant which is open now in each of the types.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            List of available restaurant types.

        """
        curs.execute("SELECT DISTINCT restaurant_type FROM restaurants "
                     "WHERE restaurant_is_open=TRUE ORDER BY restaurant_type")
        restaurant_types = curs.fetchall()
        return restaurant_types if restaurant_types else []

    @cursor
    @logger_decorator
    def show_restaurants(self, curs: psycopg2.extensions.cursor) -> List[Tuple[Any, ...]]:
        """Get list of open restaurants in chosen restaurant type.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            List of available restaurants.

        """
        callback_data = self.data_to_read.data
        curs.execute("SELECT restaurant_name, restaurant_uuid FROM restaurants "
                     "WHERE restaurant_type = %s AND restaurant_is_open = TRUE",
                     (callback_data,))
        restaurants = curs.fetchall()
        return restaurants if restaurants else []

    @cursor
    @logger_decorator
    def show_dish_categories(self, curs: psycopg2.extensions.cursor) -> List[Tuple[Any, ...]]:
        """Get list of available dish categories in the chosen restaurant.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            List of available dish categories.

        """
        callback_data = self.data_to_read.data
        curs.execute("SELECT DISTINCT category FROM dishes "
                     "WHERE restaurant_uuid = %s AND dish_is_available = TRUE",
                     (callback_data,))
        categories = curs.fetchall()
        return categories if categories else []

    @cursor
    @logger_decorator
    def show_dishes(self, curs: psycopg2.extensions.cursor) -> List[Tuple[Any, ...]]:
        """Get list of available dishes in specified category and restaurant.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            List of available dishes.

        """
        restaurant_uuid = self.get_from_cart("restaurant_uuid")
        callback_data = self.data_to_read.data
        curs.execute("SELECT dish_name, dish_uuid FROM dishes "
                     "WHERE restaurant_uuid = %s AND dish_is_available = TRUE AND category = %s",
                     (restaurant_uuid, callback_data))
        dishes = curs.fetchall()
        return dishes if dishes else []

    @cursor
    @logger_decorator
    def rest_name_by_uuid(self, curs: psycopg2.extensions.cursor) -> str:
        """Get restaurant name by its UUID.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Restaurant name.

        """
        callback_data = self.data_to_read.data
        curs.execute("SELECT restaurant_name FROM restaurants WHERE restaurant_uuid = %s",
                     (callback_data,))
        rest_name = curs.fetchone()
        return rest_name[0] if rest_name[0] else ""

    @cursor
    @logger_decorator
    def get_dish(self, curs: psycopg2.extensions.cursor) -> Tuple[Any, ...]:
        """Get dish info (name, description and price) by given dish UUID.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Array with dish info.

        """
        callback_data = self.data_to_read.data
        curs.execute("SELECT dish_name, dish_description, dish_price FROM dishes WHERE dish_uuid = %s",
                     (callback_data,))
        dish = curs.fetchone()
        return dish if dish else tuple()

    @cursor
    @logger_decorator
    def new_cart(self, curs: psycopg2.extensions.cursor) -> None:
        """Create new cart in the DB.cart table and add Customer's Telegram ID in it.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("INSERT INTO cart (customer_id) VALUES (%s)", (customer_id,))

    @cursor
    @logger_decorator
    def add_to_cart(self, column_name: str, curs: psycopg2.extensions.cursor) -> None:
        """Add required info into cart.

        Args:
            column_name: Name of column containing required info.
            curs: Cursor object from psycopg2 module.

        """
        callback_data = self.data_to_read.data
        customer_id = self.data_to_read.from_user.id
        curs.execute("UPDATE cart SET " + column_name + " = %s WHERE customer_id = %s",
                     (callback_data, customer_id))

    @cursor
    @logger_decorator
    def get_from_cart(self, column_name: str, curs: psycopg2.extensions.cursor) -> float | int | str | List[Any]:
        """Get required info from cart.

        Args:
            column_name: Name of column containing required info.
            curs: Cursor object from psycopg2 module.

        Returns:
            Required info.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("SELECT " + column_name + " FROM cart WHERE customer_id = %s", (customer_id,))
        value = curs.fetchone()
        return value[0] if value else ""

    @cursor
    @logger_decorator
    def delete_from_cart(self, column_name: str, curs: psycopg2.extensions.cursor) -> None:
        """Delete required info from cart.

        Args:
            column_name: Name of column containing required info.
            curs: Cursor object from psycopg2 module.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("UPDATE cart SET " + column_name + " = null WHERE customer_id = %s", (customer_id,))

    @cursor
    @logger_decorator
    def delete_cart(self, curs: psycopg2.extensions.cursor) -> None:
        """Delete cart connected to given Customer's Telegram ID.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("DELETE FROM cart WHERE customer_id = %s", (customer_id,))

    @cursor
    @logger_decorator
    def check_if_location(self, curs: psycopg2.extensions.cursor) -> Dict[str, float]:
        """Check if Customer's location is provided and return it if so.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Customer's longitude and latitude if ones are provided.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("SELECT customer_location FROM customers WHERE customer_id = %s", (customer_id,))
        if latlon := curs.fetchone()[0]:
            location = {"lat": latlon[0], "lon": latlon[1]}
            return location
        return {}

    @cursor
    @logger_decorator
    def get_customer_lang(self, curs: psycopg2.extensions.cursor) -> str:
        """Get code of Customer's chosen language.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Code of Customer's chosen language
            if Customer has chosen one,
            otherwise default language code, set in .env.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("SELECT lang_code FROM customers WHERE customer_id = %s", (customer_id,))
        if customer_lang := curs.fetchone():
            if customer_lang := customer_lang[0]:
                return customer_lang
        return DEF_LANG

    @cursor
    @logger_decorator
    def set_customer_lang(self, curs: psycopg2.extensions.cursor) -> None:
        """Set language code for Customer.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        customer_id = self.data_to_read.from_user.id
        lang_code = self.data_to_read.data
        curs.execute("UPDATE customers SET lang_code = %s WHERE customer_id = %s",
                     (lang_code, customer_id))

    @staticmethod
    @cursor
    @logger_decorator
    def get_restaurant_lang(rest_uuid: str, curs: psycopg2.extensions.cursor) -> str:
        """Get language code of Restaurant.

        Args:
            rest_uuid: Restaurant UUID.
            curs: Cursor object from psycopg2 module.

        Returns:
            Restaurant language code,
            if Restaurant has chosen one,
            otherwise default language code, set in .env.

        """
        curs.execute("SELECT lang_code FROM restaurants WHERE restaurant_uuid = %s", (rest_uuid,))
        if rest_lang := curs.fetchone():
            if rest_lang := rest_lang[0]:
                return rest_lang
        return DEF_LANG

    @cursor
    @logger_decorator
    def order_creation(self, curs: psycopg2.extensions.cursor) -> List[Any]:
        """Create order in database, transferring data from Customer's cart.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Array containing order information.

        """
        customer_id = self.data_to_read.from_user.id
        curs.execute("SELECT restaurant_uuid, dishes_uuids, subtotal, service_fee, courier_fee, total FROM cart "
                     "WHERE customer_id = %s",
                     (customer_id,))
        order_data = curs.fetchone()
        rest_uuid = order_data[0]
        curs.execute("SELECT restaurant_tg_id FROM restaurants WHERE restaurant_uuid = %s", (rest_uuid,))
        rest_id = curs.fetchone()[0]
        dishes_uuids = order_data[1]
        subtotal = order_data[2]
        service_fee = order_data[3]
        courier_fee = order_data[4]
        total = order_data[5]
        curs.execute("SELECT restaurant_name FROM restaurants WHERE restaurant_uuid = %s", (rest_uuid,))
        rest_name = curs.fetchone()[0]
        curs.execute("SELECT customer_name, customer_location FROM customers WHERE customer_id = %s",
                     (customer_id,))
        customer_info = curs.fetchone()
        customer_name = customer_info[0]
        customer_location = customer_info[1]
        dishes = []
        for dish_uuid in dishes_uuids:
            curs.execute("SELECT dish_name FROM dishes WHERE dish_uuid = %s", (dish_uuid,))
            current_dish = curs.fetchone()[0]
            dishes += [current_dish]
        order_uuid = str(uuid.uuid4())
        order_creation_datetime = datetime.datetime.now()
        curs.execute("INSERT INTO orders (order_uuid, restaurant_uuid, restaurant_id, restaurant_name, "
                     "customer_id, customer_name, delivery_location, dishes, dishes_subtotal, "
                     "courier_fee, service_fee, total, order_open_date, order_status, courier_id) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, -1)",
                     (order_uuid,
                      rest_uuid,
                      rest_id,
                      rest_name,
                      self.data_to_read.from_user.id,
                      customer_name,
                      customer_location,
                      dishes,
                      subtotal,
                      courier_fee,
                      service_fee,
                      total,
                      order_creation_datetime,
                      "Created"))
        order_info = [order_uuid,
                      rest_uuid,
                      rest_id,
                      rest_name,
                      self.data_to_read.from_user.id,
                      customer_name,
                      customer_location,
                      dishes,
                      subtotal,
                      courier_fee,
                      service_fee,
                      total,
                      order_creation_datetime,
                      "Created"]
        return order_info

    @staticmethod
    @cursor
    @logger_decorator
    def update_order(order_uuid: str, column: str, new_value: str, curs: psycopg2.extensions.cursor) -> None:
        """Update order information in database.

        Args:
            order_uuid: Order UUID.
            column: Required column name.
            new_value: Required new value.
            curs: Cursor object from psycopg2 module.

        """
        curs.execute("UPDATE orders SET " + column + " = %s WHERE order_uuid = %s", (new_value, order_uuid))

    @cursor
    @logger_decorator
    def get_support_id(self, curs: psycopg2.extensions.cursor) -> int:
        """Get random Admin Telegram ID from database.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Admin Telegram ID.

        """
        curs.execute("SELECT admin_id FROM admins")
        if admin_ids := curs.fetchall():
            return random.choice(admin_ids)[0]

    @staticmethod
    @cursor
    @logger_decorator
    def get_adm_lang(admin_id: int, curs: psycopg2.extensions.cursor) -> str:
        """Get Admin language code.

        Args:
            admin_id: Admin Telegram ID.
            curs: Cursor object from psycopg2 module.

        Returns:
            Admin language code.

        """
        curs.execute("SELECT lang_code FROM admins WHERE admin_id = %s", (admin_id,))
        lang_code = curs.fetchone()[0]
        return lang_code

    @staticmethod
    @cursor
    @logger_decorator
    def get_order_info(order_uuid: str, column: str, curs: psycopg2.extensions.cursor) -> str | int:
        """Get required order information from database.

        Args:
            order_uuid: Order UUID.
            column: Required column name.
            curs: Cursor object from psycopg2 module.

        Returns:
            Required order information.

        """
        curs.execute("SELECT " + column + " FROM orders WHERE order_uuid = %s", (order_uuid,))
        order_info = curs.fetchone()[0]
        return order_info

    @cursor
    @logger_decorator
    def close_order(self, curs: psycopg2.extensions.cursor) -> None:
        """Close order in database.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("UPDATE orders SET order_status = 'Order closed', order_close_date = %s "
                     "WHERE order_uuid = %s",
                     (datetime.datetime.now(), order_uuid))
        curs.execute("SELECT courier_id FROM orders WHERE order_uuid = %s", (order_uuid,))
        courier_id = curs.fetchone()[0]
        curs.execute("SELECT account_balance FROM couriers WHERE courier_id = %s", (courier_id,))
        current_balance = curs.fetchone()[0]
        curs.execute("SELECT courier_fee FROM orders WHERE order_uuid = %s", (order_uuid,))
        to_be_added = curs.fetchone()[0]
        new_balance = round(current_balance + to_be_added, 2)
        curs.execute("UPDATE couriers SET account_balance = %s, is_occupied = false WHERE courier_id = %s",
                     (new_balance, courier_id))

    @cursor
    @logger_decorator
    def delete_order(self, curs: psycopg2.extensions.cursor) -> None:
        """Delete order from database.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("DELETE FROM orders WHERE order_uuid = %s", (order_uuid,))
