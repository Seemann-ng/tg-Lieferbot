from typing import Dict, List

import psycopg2
import telebot.types as types
from environs import Env

from loggertool import logger

env = Env()
env.read_env()

DB = env.str("DB")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")


# TODO: make it a decorator.
def cursor():
    conn = psycopg2.connect(
        database=DB,
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    return cur


class DBInterface:
    @staticmethod
    def user_in_db(message: types.Message) -> str | None:
        """Check if Customer is in the DB and if so get their name or Telegram username.

        Args:
            message: Message from Customer.

        Returns:
            Customer name from the DB if Customer is in the DB and has provided their name,
            Telegram username if Customer is in the DB and has NOT provided their name.

        """
        cur = cursor()
        cur.execute(
            "SELECT customer_name, customer_username FROM customers WHERE customers.customer_id = %s",
            (message.from_user.id,)
        )
        customer_names = cur.fetchone()
        cur.connection.close()
        if customer_names:
            if customer_names[0]:
                return customer_names[0]
            return customer_names[1]

    @classmethod
    def add_customer(cls, message: types.Message) -> None:
        """

        Args:
            message:

        """
        cur = cursor()
        if not cls.user_in_db(message):
            cur.execute(
                "INSERT INTO customers (customer_id, customer_username) VALUES (%s, %s)",
                (message.from_user.id, message.from_user.username)
            )
            cur.connection.commit()
        cur.connection.close()

    @staticmethod
    def update_name(message: types.Message) -> None:
        """

        Args:
            message:

        """
        cur = cursor()
        cur.execute(
            "UPDATE customers SET customer_name = %s WHERE customers.customer_id = %s",
            (message.text, message.from_user.id)
        )
        cur.connection.commit()
        cur.connection.close()

    @staticmethod
    def update_phone_number(customer_id: int, phone_number: str) -> None:
        """

        Args:
            customer_id:
            phone_number:

        """
        cur = cursor()
        cur.execute(
            "UPDATE customers SET customer_phone_num = %s WHERE customers.customer_id = %s",
            (phone_number, customer_id)
        )
        cur.connection.commit()
        cur.connection.close()

    @staticmethod
    def update_customer_location(lat: float, lon: float, message: types.Message) -> None:
        """

        Args:
            lat:
            lon:
            message:

        """
        cur = cursor()
        cur.execute(
            "UPDATE customers SET customer_location = '{%s, %s}' WHERE customers.customer_id = %s",
            (lat, lon, message.from_user.id)
        )
        cur.connection.commit()
        cur.connection.close()

    @staticmethod
    def delete_customer(message: types.Message) -> None:
        """

        Args:
            message:

        """
        cur = cursor()
        cur.execute(
            "DELETE FROM customers WHERE customers.customer_id = %s",
            (message.from_user.id,)
        )
        cur.connection.commit()
        cur.connection.close()

    @staticmethod
    def show_my_orders(message: types.Message) -> List | None:
        """

        Args:
            message:

        Returns:

        """
        cur = cursor()
        cur.execute(
            "SELECT order_uuid, restaurant_name, courier_name, dishes, total, order_date, order_status "
            "FROM orders WHERE orders.customer_id = %s",
            (message.from_user.id,)
        )
        orders = cur.fetchall()
        cur.connection.close()
        return orders

    @staticmethod
    def show_restaurant_types() -> List | None:
        """

        Returns:

        """
        cur = cursor()
        cur.execute("SELECT DISTINCT restaurant_type FROM restaurants WHERE restaurants.restaurant_is_open=TRUE"
                    " ORDER BY restaurant_type")
        restaurant_types = cur.fetchall()
        cur.connection.close()
        return restaurant_types

    @staticmethod
    def show_restaurants(restaurant_type: str) -> List | None:
        """

        Args:
            restaurant_type:

        Returns:

        """
        cur = cursor()
        cur.execute(
            "SELECT restaurant_name, restaurant_uuid FROM restaurants WHERE restaurants.restaurant_type = %s AND restaurants.restaurant_is_open = TRUE",
            (restaurant_type,)
        )
        restaurants = cur.fetchall()
        cur.connection.close()
        return restaurants

    @staticmethod
    def show_dish_categories(restaurant_uuid: str) -> List | None:
        """

        Args:
            restaurant_uuid:

        Returns:

        """
        cur = cursor()
        cur.execute(
            "SELECT DISTINCT category FROM dishes WHERE dishes.restaurant_uuid = %s AND dishes.dish_is_available = TRUE",
            (restaurant_uuid,)
        )
        categories = cur.fetchall()
        cur.connection.close()
        return categories

    @classmethod
    def show_dishes(cls, call: types.CallbackQuery) -> List | None:
        """"""
        cur = cursor()
        restaurant_uuid = cls.get_from_cart("restaurant_uuid",call)
        cur.execute(
            "SELECT dish_name, dish_uuid FROM dishes WHERE dishes.restaurant_uuid = %s AND dishes.dish_is_available = TRUE AND dishes.category = %s",
            (restaurant_uuid, call.data)
        )
        dishes = cur.fetchall()
        cur.connection.close()
        return dishes

    @staticmethod
    def rest_name_by_uuid(rest_uuid: str) -> str | None:
        """

        Args:
            rest_uuid:

        Returns:

        """
        cur = cursor()
        cur.execute(
            "SELECT restaurant_name FROM restaurants WHERE restaurants.restaurant_uuid = %s",
            (rest_uuid,)
        )
        rest_name = cur.fetchone()
        return rest_name[0]
    @staticmethod
    def get_dish(call: types.CallbackQuery) -> List | None:
        """"""
        cur = cursor()
        cur.execute(
            "SELECT dish_name, dish_description, dish_price FROM dishes WHERE dishes.dish_uuid = %s",
            (call.data,)
        )
        dish = cur.fetchone()
        cur.connection.close()
        return dish

    @staticmethod
    def new_cart(call: types.CallbackQuery) -> None:
        """"""
        cur = cursor()
        cur.execute("INSERT INTO cart (customer_id) VALUES (%s)", (call.from_user.id,))
        cur.connection.commit()
        cur.connection.close()

    @staticmethod
    def add_to_cart(column_name: str, call: types.CallbackQuery) -> None:
        """"""
        cur = cursor()
        cur.execute(
            "UPDATE cart SET " + column_name + " =%s WHERE cart.customer_id = %s",
            (call.data, call.from_user.id)
        )
        cur.connection.commit()
        cur.connection.close()

    @staticmethod
    def get_from_cart(column_name: str, call: types.CallbackQuery) -> str | List | None:
        """"""
        cur = cursor()
        cur.execute("SELECT " + column_name + " FROM cart WHERE cart.customer_id = %s", (call.from_user.id,))
        value = cur.fetchone()
        return value

    @staticmethod
    def delete_from_cart(column_name: str, call: types.CallbackQuery) -> None:
        """"""
        cur = cursor()
        cur.execute("UPDATE cart SET " + column_name + " =null WHERE cart.customer_id = %s", (call.from_user.id,))
        cur.connection.commit()
        cur.connection.close()

    @staticmethod
    def delete_cart(uid) -> None:
        """

        Args:
            uid:

        Returns:

        """
        cur = cursor()
        cur.execute("DELETE FROM cart WHERE cart.customer_id = %s", (uid,))
        cur.connection.commit()
        cur.connection.close()

    @staticmethod
    def check_if_location(message: types.Message) -> Dict[str, float] | None:
        """

        Args:
            message:

        Returns:

        """
        cur = cursor()
        cur.execute(
            "SELECT customer_location FROM customers WHERE customers.customer_id = %s",
            (message.from_user.id,)
        )
        latlon = cur.fetchone()
        cur.connection.close()
        if latlon[0]:
            location = {
                "lat": latlon[0][0],
                "lon": latlon[0][1]
            }
            return location
