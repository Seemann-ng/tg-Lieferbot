from typing import Dict, List, Tuple, Any

import psycopg2
import telebot.types as types
from environs import Env

from loggertool import logger_decorator, logger_decorator_callback, logger_decorator_msg

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
    @logger_decorator_msg
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
    @logger_decorator_msg
    def add_customer(cls, message: types.Message) -> None:
        """Add Customer to DB.

        Args:
            message: Message from Customer.

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
    @logger_decorator_msg
    def update_name(message: types.Message) -> None:
        """Update Customer Name in the DB.

        Args:
            message: Message from Customer containing their name.

        """
        cur = cursor()
        cur.execute(
            "UPDATE customers SET customer_name = %s WHERE customers.customer_id = %s",
            (message.text, message.from_user.id)
        )
        cur.connection.commit()
        cur.connection.close()

    @staticmethod
    @logger_decorator
    def update_phone_number(customer_id: int, phone_number: str) -> None:
        """Update Customer Phone Number in the DB.

        Args:
            customer_id: Customer's Telegram user ID.
            phone_number: Customer's Phone Number.

        """
        cur = cursor()
        cur.execute(
            "UPDATE customers SET customer_phone_num = %s WHERE customers.customer_id = %s",
            (phone_number, customer_id)
        )
        cur.connection.commit()
        cur.connection.close()

    @staticmethod
    @logger_decorator
    def update_customer_location(lat: float, lon: float, message: types.Message) -> None:
        """Update Customer Location in the DB.

        Args:
            lat: Customer's Latitude.
            lon: Customer's Longitude.
            message: Message from Customer.

        """
        cur = cursor()
        cur.execute(
            "UPDATE customers SET customer_location = '{%s, %s}' WHERE customers.customer_id = %s",
            (lat, lon, message.from_user.id)
        )
        cur.connection.commit()
        cur.connection.close()

    @staticmethod
    @logger_decorator_msg
    def delete_customer(message: types.Message) -> None:
        """Delete Customer from the DB.

        Args:
            message: Message from Customer.

        """
        cur = cursor()
        cur.execute(
            "DELETE FROM customers WHERE customers.customer_id = %s",
            (message.from_user.id,)
        )
        cur.connection.commit()
        cur.connection.close()

    @staticmethod
    @logger_decorator_msg
    def show_my_orders(message: types.Message) -> List[Tuple[Any, ...]] | None:
        """Get list of Customer's orders.

        Args:
            message: Message from Customer.

        Returns:
            List of tuples with Customer's orders info inside them.

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
    @logger_decorator
    def show_restaurant_types() -> List[Tuple[Any, ...]] | None:
        """Get list of restaurant types containing at least one restaurant which is open now in each of the types.

        Returns:
            List of available restaurant types.

        """
        cur = cursor()
        cur.execute("SELECT DISTINCT restaurant_type FROM restaurants WHERE restaurants.restaurant_is_open=TRUE"
                    " ORDER BY restaurant_type")
        restaurant_types = cur.fetchall()
        cur.connection.close()
        return restaurant_types

    @staticmethod
    @logger_decorator
    def show_restaurants(restaurant_type: str) -> List[Tuple[Any, ...]] | None:
        """Get list of open restaurants in chosen restaurant type.

        Args:
            restaurant_type: Chosen restaurant type.

        Returns:
            List of available restaurants.

        """
        cur = cursor()
        cur.execute(
            "SELECT restaurant_name, restaurant_uuid FROM restaurants "
            "WHERE restaurants.restaurant_type = %s AND restaurants.restaurant_is_open = TRUE",
            (restaurant_type,)
        )
        restaurants = cur.fetchall()
        cur.connection.close()
        return restaurants

    @staticmethod
    @logger_decorator
    def show_dish_categories(restaurant_uuid: str) -> List[Tuple[Any, ...]] | None:
        """Get list of available dish categories in the chosen restaurant.

        Args:
            restaurant_uuid: Restaurant UUID.

        Returns:
            List of available dish categories.

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
    @logger_decorator_callback
    def show_dishes(cls, call: types.CallbackQuery) -> List[Tuple[Any, ...]] | None:
        """Get list of available dishes in specified category and restaurant.

        Args:
            call: Callback query from Customer.

        Returns:
            List of available dishes.

        """
        cur = cursor()
        restaurant_uuid = cls.get_from_cart("restaurant_uuid", call)
        cur.execute(
            "SELECT dish_name, dish_uuid FROM dishes WHERE dishes.restaurant_uuid = %s AND dishes.dish_is_available = TRUE AND dishes.category = %s",
            (restaurant_uuid, call.data)
        )
        dishes = cur.fetchall()
        cur.connection.close()
        return dishes

    @staticmethod
    @logger_decorator
    def rest_name_by_uuid(rest_uuid: str) -> str | None:
        """Get restaurant name by its UUID.

        Args:
            rest_uuid: Restaurant UUID.

        Returns:
            Restaurant name.

        """
        cur = cursor()
        cur.execute(
            "SELECT restaurant_name FROM restaurants WHERE restaurants.restaurant_uuid = %s",
            (rest_uuid,)
        )
        rest_name = cur.fetchone()
        return rest_name[0]

    @staticmethod
    @logger_decorator_callback
    def get_dish(call: types.CallbackQuery) -> Tuple[Any, ...] | None:
        """Get dish info (name, description and price) by given dish UUID.

        Args:
            call: Callback query from Customer.

        Returns:
            Tuple with dish info.

        """
        cur = cursor()
        cur.execute(
            "SELECT dish_name, dish_description, dish_price FROM dishes WHERE dishes.dish_uuid = %s",
            (call.data,)
        )
        dish = cur.fetchone()
        cur.connection.close()
        return dish

    @staticmethod
    @logger_decorator_callback
    def new_cart(call: types.CallbackQuery) -> None:
        """Create new cart in the DB.cart table and add Customer's Telegram ID in it.

        Args:
            call: Callback query from Customer.

        """
        cur = cursor()
        cur.execute("INSERT INTO cart (customer_id) VALUES (%s)", (call.from_user.id,))
        cur.connection.commit()
        cur.connection.close()

    @staticmethod
    @logger_decorator
    def add_to_cart(column_name: str, call: types.CallbackQuery) -> None:
        """Add required info into cart.

        Args:
            column_name: Name of column containing required info.
            call: Callback query from Customer.

        """
        cur = cursor()
        cur.execute(
            "UPDATE cart SET " + column_name + " =%s WHERE cart.customer_id = %s",
            (call.data, call.from_user.id)
        )
        cur.connection.commit()
        cur.connection.close()

    @staticmethod
    @logger_decorator
    def get_from_cart(column_name: str, call: types.CallbackQuery) -> float | int | str | List[Any] | None:
        """Get required info from cart.

        Args:
            column_name: Name of column containing required info.
            call: Callback query from Customer.

        Returns:
            Required info.

        """
        cur = cursor()
        cur.execute("SELECT " + column_name + " FROM cart WHERE cart.customer_id = %s", (call.from_user.id,))
        value = cur.fetchone()
        return value[0] if value is not None else None

    @staticmethod
    @logger_decorator
    def delete_from_cart(column_name: str, call: types.CallbackQuery) -> None:
        """Delete required info from cart.

        Args:
            column_name: Name of column containing required info.
            call: callback query from Customer.

        """
        cur = cursor()
        cur.execute("UPDATE cart SET " + column_name + " =null WHERE cart.customer_id = %s", (call.from_user.id,))
        cur.connection.commit()
        cur.connection.close()

    @staticmethod
    @logger_decorator
    def delete_cart(uid: int) -> None:
        """Delete cart connected to given Customer's Telegram ID.

        Args:
            uid: Customer's Telegram ID.

        """
        cur = cursor()
        cur.execute("DELETE FROM cart WHERE cart.customer_id = %s", (uid,))
        cur.connection.commit()
        cur.connection.close()

    @staticmethod
    @logger_decorator_msg
    def check_if_location(message: types.Message) -> Dict[str, float] | None:
        """Check if Customer's location is provided and return it if so.

        Args:
            message: Message from Customer.

        Returns:
            Customer's longitude and latitude if ones are provided.

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
