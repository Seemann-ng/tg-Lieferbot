import uuid
import random
import datetime
from typing import Any, Dict, List, Tuple

import telebot.types as types
from environs import Env
from geopy.distance import geodesic
from psycopg2.extensions import cursor

from tools.cursor_tool import cursor as cursor_decorator
from tools.logger_tool import logger, logger_decorator

env = Env()
env.read_env()

DEF_LANG = env.str("DEF_LANG", default="en_US")


class Interface:
    def __init__(self, data_to_read: types.Message | types.CallbackQuery):
        self.data_to_read = data_to_read
        logger.info(f"Interface instance initialized with {type(self.data_to_read)}.")

    @cursor_decorator
    @logger_decorator
    def user_in_db(self, curs: cursor) -> str | None:
        """Check if Customer is in the DB and if so get their name
         or Telegram username.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Customer name from the DB if Customer is in the DB and
            has provided their name, Telegram username if Customer is
            in the DB and has NOT provided their name.

        """
        curs.execute(
            "SELECT customer_name, customer_username FROM customers WHERE customer_id = %s",
            (self.data_to_read.from_user.id,)
        )
        if customer_names := curs.fetchone():
            if customer_names[0]:
                return customer_names[0]
            return customer_names[1]

    @cursor_decorator
    @logger_decorator
    def add_customer(self, curs: cursor) -> None:
        """Add Customer to DB.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        if self.user_in_db():
            return None
        curs.execute(
            "INSERT INTO customers (customer_id, customer_username) VALUES (%s, %s)",
            (self.data_to_read.from_user.id, self.data_to_read.from_user.username)
        )

    @cursor_decorator
    @logger_decorator
    def update_name(self, curs: cursor) -> None:
        """Update Customer name in the DB.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        curs.execute(
            "UPDATE customers SET customer_name = %s WHERE customer_id = %s",
            (self.data_to_read.text, self.data_to_read.from_user.id)
        )

    @cursor_decorator
    @logger_decorator
    def update_phone_number(self, phone_number: str, curs: cursor) -> None:
        """Update Customer phone number in the DB.

        Args:
            phone_number: Customer's phone number.
            curs: Cursor object from psycopg2 module.

        """
        curs.execute(
            "UPDATE customers SET customer_phone_num = %s WHERE customer_id = %s",
            (phone_number, self.data_to_read.from_user.id)
        )

    @cursor_decorator
    @logger_decorator
    def update_customer_location(self, curs: cursor) -> None:
        """Update Customer Location in the DB.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        curs.execute(
            "UPDATE customers SET customer_location = '{%s, %s}' WHERE customer_id = %s",
            (
                self.data_to_read.location.latitude,
                self.data_to_read.location.longitude,
                self.data_to_read.from_user.id
            )
        )

    @cursor_decorator
    @logger_decorator
    def delete_customer(self, curs: cursor) -> None:
        """Delete Customer from the DB.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        curs.execute(
            "DELETE FROM customers WHERE customer_id = %s",
            (self.data_to_read.from_user.id,)
        )

    @cursor_decorator
    @logger_decorator
    def show_my_orders(self, curs: cursor) -> List[Tuple[Any, ...]]:
        """Get list of Customer's orders.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            List of tuples with Customer's orders info inside them.

        """
        curs.execute(
            "SELECT order_uuid, restaurant_name, courier_name, dishes, total, order_open_date, "
            "order_status, order_close_date FROM orders WHERE customer_id = %s",
            (self.data_to_read.from_user.id,)
        )
        orders = [] or curs.fetchall()
        return orders

    @staticmethod
    @cursor_decorator
    @logger_decorator
    def show_restaurant_types(curs: cursor) -> List[Tuple[Any, ...]]:
        """Get list of restaurant types containing at least one
        restaurant which is open now in each of the types.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            List of available restaurant types.

        """
        curs.execute(
            "SELECT DISTINCT restaurant_type FROM restaurants WHERE restaurant_is_open=TRUE "
            "ORDER BY restaurant_type"
        )
        restaurant_types = [] or curs.fetchall()
        return restaurant_types

    @cursor_decorator
    @logger_decorator
    def show_restaurants(self, curs: cursor) -> List[Tuple[Any, ...]]:
        """Get list of open restaurants in chosen restaurant type.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            List of available restaurants.

        """
        curs.execute(
            "SELECT restaurant_name, restaurant_uuid FROM restaurants "
            "WHERE restaurant_type = %s AND restaurant_is_open = TRUE",
            (self.data_to_read.data,)
        )
        restaurants = [] or curs.fetchall()
        return restaurants

    @cursor_decorator
    @logger_decorator
    def show_dish_categories(self, curs: cursor) -> List[Tuple[Any, ...]]:
        """Get list of available dish categories in the chosen
        restaurant.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            List of available dish categories.

        """
        curs.execute(
            "SELECT DISTINCT category FROM dishes "
            "WHERE restaurant_uuid = %s AND dish_is_available = TRUE",
            (self.data_to_read.data,)
        )
        categories = [] or curs.fetchall()
        return categories

    @cursor_decorator
    @logger_decorator
    def show_dishes(self, curs: cursor) -> List[Tuple[Any, ...]]:
        """Get list of available dishes in specified category
        and restaurant.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            List of available dishes.

        """
        curs.execute(
            "SELECT dish_name, dish_uuid FROM dishes "
            "WHERE restaurant_uuid = %s AND dish_is_available = TRUE AND category = %s",
            (self.get_from_cart("restaurant_uuid"), self.data_to_read.data)
        )
        dishes = [] or curs.fetchall()
        return dishes

    @cursor_decorator
    @logger_decorator
    def rest_name_by_uuid(self, curs: cursor) -> str:
        """Get restaurant name by its UUID.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Restaurant name.

        """
        curs.execute(
            "SELECT restaurant_name FROM restaurants WHERE restaurant_uuid = %s",
            (self.data_to_read.data,)
        )
        rest_name = curs.fetchone()
        return rest_name[0] if rest_name[0] else ""

    @cursor_decorator
    @logger_decorator
    def get_dish(self, curs: cursor) -> Tuple[Any, ...]:
        """Get dish info (name, description and price) by given dish
        UUID.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Array with dish info.

        """
        curs.execute(
            "SELECT dish_name, dish_description, dish_price FROM dishes WHERE dish_uuid = %s",
            (self.data_to_read.data,)
        )
        dish = tuple() or curs.fetchone()
        return dish

    @staticmethod
    @cursor_decorator
    @logger_decorator
    def check_couriers(curs: cursor) -> List[Tuple[Any, ...]]:
        """Check if there is at least one courier available.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            List of available couriers.

        """
        curs.execute(
            "SELECT courier_id FROM couriers WHERE courier_status = TRUE AND is_occupied = FALSE"
        )
        couriers = [] or curs.fetchall()
        return couriers

    @cursor_decorator
    @logger_decorator
    def new_cart(self, curs: cursor) -> None:
        """Create new cart in the DB.cart table and add Customer's
        Telegram ID in it.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        curs.execute(
            "INSERT INTO cart (customer_id) VALUES (%s)", (self.data_to_read.from_user.id,)
        )

    @cursor_decorator
    @logger_decorator
    def add_to_cart(self, column_name: str, curs: cursor) -> None:
        """Add required info into cart.

        Args:
            column_name: Name of column containing required info.
            curs: Cursor object from psycopg2 module.

        """
        curs.execute(
            "UPDATE cart SET " + column_name + " = %s WHERE customer_id = %s",
            (self.data_to_read.data, self.data_to_read.from_user.id)
        )

    @cursor_decorator
    @logger_decorator
    def get_from_cart(self, column_name: str, curs: cursor) -> float | int | str | List[Any]:
        """Get required info from cart.

        Args:
            column_name: Name of column containing required info.
            curs: Cursor object from psycopg2 module.

        Returns:
            Required info.

        """
        curs.execute(
            "SELECT " + column_name + " FROM cart WHERE customer_id = %s",
            (self.data_to_read.from_user.id,)
        )
        value = "" or curs.fetchone()
        return value[0]

    @cursor_decorator
    @logger_decorator
    def get_delivery_distance(self, curs: cursor) -> float:
        """Calculate delivery distance based on data in database.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Delivery distance in kilometers with two digits precision.

        """
        customer_location_dict = self.check_if_location()
        customer_location = (
            float(customer_location_dict["lat"]),
            float(customer_location_dict["lon"])
        )
        curs.execute(
            "SELECT restaurant_uuid FROM cart WHERE customer_id = %s",
            (self.data_to_read.from_user.id,)
        )
        rest_uuid = curs.fetchone()
        curs.execute("SELECT location FROM restaurants WHERE restaurant_uuid = %s", (rest_uuid,))
        rest_location_list = curs.fetchone()[0]
        rest_location = (float(rest_location_list[0]), float(rest_location_list[1]))
        delivery_distance = round(float(geodesic(rest_location, customer_location).km), 2)
        return delivery_distance

    @cursor_decorator
    @logger_decorator
    def delete_from_cart(self, column_name: str, curs: cursor) -> None:
        """Delete required info from cart.

        Args:
            column_name: Name of column containing required info.
            curs: Cursor object from psycopg2 module.

        """
        curs.execute(
            "UPDATE cart SET " + column_name + " = null WHERE customer_id = %s",
            (self.data_to_read.from_user.id,)
        )

    @cursor_decorator
    @logger_decorator
    def delete_cart(self, curs: cursor) -> None:
        """Delete cart connected to given Customer's Telegram ID.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        curs.execute("DELETE FROM cart WHERE customer_id = %s", (self.data_to_read.from_user.id,))

    @cursor_decorator
    @logger_decorator
    def check_if_location(self, curs: cursor) -> Dict[str, float]:
        """Check if Customer's location is provided and return it if so.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Customer's longitude and latitude if ones are provided.

        """
        curs.execute(
            "SELECT customer_location FROM customers WHERE customer_id = %s",
            (self.data_to_read.from_user.id,)
        )
        if latlon := curs.fetchone()[0]:
            return {"lat": latlon[0], "lon": latlon[1]}
        return {}

    @cursor_decorator
    @logger_decorator
    def get_customer_lang(self, curs: cursor) -> str:
        """Get code of Customer's chosen language.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Code of Customer's chosen language if Customer has chosen
            one, otherwise default language code, set in .env.

        """
        curs.execute(
            "SELECT lang_code FROM customers WHERE customer_id = %s",
            (self.data_to_read.from_user.id,)
        )
        lang = DEF_LANG
        if customer_lang := curs.fetchone():
            lang = customer_lang[0] or lang
        return lang

    @cursor_decorator
    @logger_decorator
    def set_customer_lang(self, curs: cursor) -> None:
        """Set language code for Customer.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        curs.execute(
            "UPDATE customers SET lang_code = %s WHERE customer_id = %s",
            (self.data_to_read.data, self.data_to_read.from_user.id)
        )

    @staticmethod
    @cursor_decorator
    @logger_decorator
    def get_restaurant_lang(rest_uuid: str, curs: cursor) -> str:
        """Get language code of Restaurant.

        Args:
            rest_uuid: Restaurant UUID.
            curs: Cursor object from psycopg2 module.

        Returns:
            Restaurant language code, if Restaurant has chosen one,
            otherwise default language code, set in .env.

        """
        curs.execute("SELECT lang_code FROM restaurants WHERE restaurant_uuid = %s", (rest_uuid,))
        lang = DEF_LANG
        if restaurant_lang := curs.fetchone():
            lang = restaurant_lang[0] or lang
        return lang

    @cursor_decorator
    @logger_decorator
    def order_creation(self, curs: cursor) -> List[Any]:
        """Create order in database, transferring data from Customer's
        cart.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Array containing order information.

        """
        curs.execute(
            "SELECT restaurant_uuid, dishes_uuids, subtotal, service_fee, courier_fee, total, "
            "order_comment FROM cart WHERE customer_id = %s",
            (self.data_to_read.from_user.id,)
        )
        order_data = curs.fetchone()
        curs.execute(
            "SELECT restaurant_tg_id FROM restaurants WHERE restaurant_uuid = %s", (order_data[0],)
        )
        rest_id = curs.fetchone()[0]
        curs.execute(
            "SELECT restaurant_name FROM restaurants WHERE restaurant_uuid = %s", (order_data[0],)
        )
        rest_name = curs.fetchone()[0]
        curs.execute(
            "SELECT customer_name, customer_location FROM customers WHERE customer_id = %s",
            (self.data_to_read.from_user.id,)
        )
        customer_info = curs.fetchone()
        dishes = []
        for dish_uuid in order_data[1]:
            curs.execute(
                "SELECT dish_name FROM dishes WHERE dish_uuid = %s",
                (dish_uuid,)
            )
            current_dish = curs.fetchone()[0]
            dishes += [current_dish]
        order_uuid = str(uuid.uuid4())
        order_creation_datetime = datetime.datetime.now()
        curs.execute(
            "INSERT INTO orders (order_uuid, restaurant_uuid, restaurant_id, restaurant_name, "
            "customer_id, customer_name, delivery_location, dishes, dishes_subtotal, courier_fee, "
            "service_fee, total, order_open_date, order_status, order_comment, delivery_distance) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (order_uuid,
                order_data[0],
                rest_id,
                rest_name,
                self.data_to_read.from_user.id,
                customer_info[0],
                customer_info[1],
                dishes,
                order_data[2],
                order_data[4],
                order_data[3],
                order_data[5],
                order_creation_datetime,
                "1",
                order_data[6],
                self.get_delivery_distance()
            )
        )
        return [
            order_uuid, order_data[0], rest_id, rest_name, self.data_to_read.from_user.id,
            customer_info[0], customer_info[1], dishes, order_data[2], order_data[4],
            order_data[3], order_data[5], order_creation_datetime, "1", order_data[6]
        ]

    @staticmethod
    @cursor_decorator
    @logger_decorator
    def update_order(order_uuid: str, column: str, new_value: str, curs: cursor) -> None:
        """Update order information in database.

        Args:
            order_uuid: Order UUID.
            column: Required column name.
            new_value: Required new value.
            curs: Cursor object from psycopg2 module.

        """
        curs.execute(
            "UPDATE orders SET " + column + " = %s WHERE order_uuid = %s", (new_value, order_uuid)
        )

    @cursor_decorator
    @logger_decorator
    def get_support(self, curs: cursor) -> Tuple[int, str]:
        """Get random Admin Telegram ID and their language code from
        database.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Array containing random Admin Telegram ID and their
            language code.

        """
        curs.execute("SELECT admin_id FROM admins")
        if admin_ids := curs.fetchall():
            admin_id = random.choice(admin_ids)[0]
            curs.execute("SELECT lang_code FROM admins WHERE admin_id = %s", (admin_id,))
            if admin_lang_code := curs.fetchone()[0]:
                return admin_id, admin_lang_code
            return admin_id, DEF_LANG


    @staticmethod
    @cursor_decorator
    @logger_decorator
    def get_order_info(order_uuid: str, column: str, curs: cursor) -> str | int:
        """Get required order information from database.

        Args:
            order_uuid: Order UUID.
            column: Required column name.
            curs: Cursor object from psycopg2 module.

        Returns:
            Required order information.

        """
        curs.execute(
            "SELECT " + column + " FROM orders WHERE order_uuid = %s",  (order_uuid,)
        )
        return curs.fetchone()[0]

    @cursor_decorator
    @logger_decorator
    def close_order(self, curs: cursor) -> None:
        """Close order in database.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        curs.execute(
            "UPDATE orders SET order_status = '0', order_close_date = %s WHERE order_uuid = %s",
            (datetime.datetime.now(), self.data_to_read.data.split(maxsplit=1)[-1])
        )
        curs.execute(
            "SELECT courier_id FROM orders WHERE order_uuid = %s",
            (self.data_to_read.data.split(maxsplit=1)[-1],)
        )
        courier_id = curs.fetchone()[0]
        curs.execute(
            "SELECT account_balance FROM couriers WHERE courier_id = %s", (courier_id,)
        )
        current_balance = curs.fetchone()[0]
        curs.execute(
            "SELECT courier_fee FROM orders WHERE order_uuid = %s",
            (self.data_to_read.data.split(maxsplit=1)[-1],)
        )
        curs.execute(
            "UPDATE couriers SET account_balance = %s, is_occupied = false WHERE courier_id = %s",
            (round((current_balance + curs.fetchone()[0]), 2), courier_id)
        )
