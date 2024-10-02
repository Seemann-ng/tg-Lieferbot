from typing import Dict, List, Tuple, Any

import psycopg2
import telebot.types as types
from environs import Env

from loggertool import logger, logger_decorator

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
    def __init__(self, input_obj: types.Message | types.CallbackQuery):
        self.input_object = input_obj
        logger.info(
            f"DBInterface instance initialized with self.data = {self.input_object} of type {type(self.input_object)}."
        )

    @logger_decorator
    def user_in_db(self) -> str | None:
        """Check if Customer is in the DB and if so get their name or Telegram username.

        Returns:
            Customer name from the DB if Customer is in the DB and has provided their name,
            Telegram username if Customer is in the DB and has NOT provided their name.

        """
        cur = cursor()
        customer_id = self.input_object.from_user.id
        cur.execute(
            "SELECT customer_name, customer_username "
            "FROM customers "
            "WHERE customers.customer_id = %s",
            [customer_id]
        )
        customer_names = cur.fetchone()
        cur.connection.close()
        if customer_names:
            if customer_names[0]:
                return customer_names[0]
            return customer_names[1]

    @logger_decorator
    def add_customer(self) -> None:
        """Add Customer to DB.

        """
        cur = cursor()
        if not self.user_in_db():
            customer_id = self.input_object.from_user.id
            customer_username = self.input_object.from_user.username
            cur.execute(
                "INSERT INTO customers (customer_id, customer_username) "
                "VALUES (%s, %s)",
                [
                    customer_id,
                    customer_username
                ]
            )
            cur.connection.commit()
        cur.connection.close()

    @logger_decorator
    def update_name(self) -> None:
        """Update Customer name in the DB.

        """
        cur = cursor()
        customer_name = self.input_object.text
        customer_id = self.input_object.from_user.id
        cur.execute(
            "UPDATE customers "
            "SET customer_name = %s "
            "WHERE customers.customer_id = %s",
            [
                customer_name,
                customer_id
            ]
        )
        cur.connection.commit()
        cur.connection.close()

    @logger_decorator
    def update_phone_number(self, phone_number: str) -> None:
        """Update Customer phone number in the DB.

        Args:
            phone_number: Customer's phone number.

        """
        cur = cursor()
        customer_id = self.input_object.from_user.id
        cur.execute(
            "UPDATE customers "
            "SET customer_phone_num = %s "
            "WHERE customers.customer_id = %s",
            [
                phone_number,
                customer_id
            ]
        )
        cur.connection.commit()
        cur.connection.close()

    @logger_decorator
    def update_customer_location(self) -> None:
        """Update Customer Location in the DB.

        """
        cur = cursor()
        latitude = self.input_object.location.latitude
        longitude = self.input_object.location.longitude
        customer_id = self.input_object.from_user.id
        cur.execute(
            "UPDATE customers "
            "SET customer_location = '{%s, %s}' "
            "WHERE customers.customer_id = %s",
            [
                latitude,
                longitude,
                customer_id
            ]
        )
        cur.connection.commit()
        cur.connection.close()

    @logger_decorator
    def delete_customer(self) -> None:
        """Delete Customer from the DB.

        """
        cur = cursor()
        customer_id = self.input_object.from_user.id
        cur.execute("DELETE FROM customers WHERE customers.customer_id = %s", [customer_id])
        cur.connection.commit()
        cur.connection.close()

    @logger_decorator
    def show_my_orders(self) -> List[Tuple[Any, ...]] | None:
        """Get list of Customer's orders.

        Returns:
            List of tuples with Customer's orders info inside them.

        """
        cur = cursor()
        customer_id = self.input_object.from_user.id
        cur.execute(
            "SELECT order_uuid, restaurant_name, courier_name, dishes, total, order_date, order_status "
            "FROM orders "
            "WHERE orders.customer_id = %s",
            [
                customer_id
            ]
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
        cur.execute(
            "SELECT DISTINCT restaurant_type "
            "FROM restaurants "
            "WHERE restaurants.restaurant_is_open=TRUE "
            "ORDER BY restaurant_type"
        )
        restaurant_types = cur.fetchall()
        cur.connection.close()
        return restaurant_types

    @logger_decorator
    def show_restaurants(self) -> List[Tuple[Any, ...]] | None:
        """Get list of open restaurants in chosen restaurant type.

        Returns:
            List of available restaurants.

        """
        cur = cursor()
        callback_data = self.input_object.data
        cur.execute(
            "SELECT restaurant_name, restaurant_uuid "
            "FROM restaurants "
            "WHERE restaurants.restaurant_type = %s "
            "AND restaurants.restaurant_is_open = TRUE",
            [callback_data]
        )
        restaurants = cur.fetchall()
        cur.connection.close()
        return restaurants

    @logger_decorator
    def show_dish_categories(self) -> List[Tuple[Any, ...]] | None:
        """Get list of available dish categories in the chosen restaurant.

        Returns:
            List of available dish categories.

        """
        cur = cursor()
        callback_data = self.input_object.data
        cur.execute(
            "SELECT DISTINCT category "
            "FROM dishes "
            "WHERE dishes.restaurant_uuid = %s "
            "AND dishes.dish_is_available = TRUE",
            [callback_data]
        )
        categories = cur.fetchall()
        cur.connection.close()
        return categories

    @logger_decorator
    def show_dishes(self) -> List[Tuple[Any, ...]] | None:
        """Get list of available dishes in specified category and restaurant.

        Returns:
            List of available dishes.

        """
        cur = cursor()
        restaurant_uuid = self.get_from_cart("restaurant_uuid")
        callback_data = self.input_object.data
        cur.execute(
            "SELECT dish_name, dish_uuid "
            "FROM dishes "
            "WHERE dishes.restaurant_uuid = %s "
            "AND dishes.dish_is_available = TRUE "
            "AND dishes.category = %s",
            [
                restaurant_uuid,
                callback_data
            ]
        )
        dishes = cur.fetchall()
        cur.connection.close()
        return dishes

    @logger_decorator
    def rest_name_by_uuid(self) -> str | None:
        """Get restaurant name by its UUID.

        Returns:
            Restaurant name.

        """
        cur = cursor()
        callback_data = self.input_object.data
        cur.execute(
            "SELECT restaurant_name "
            "FROM restaurants "
            "WHERE restaurants.restaurant_uuid = %s",
            [callback_data]
        )
        rest_name = cur.fetchone()
        return rest_name[0]

    @logger_decorator
    def get_dish(self) -> Tuple[Any, ...] | None:
        """Get dish info (name, description and price) by given dish UUID.

        Returns:
            Tuple with dish info.

        """
        cur = cursor()
        callback_data = self.input_object.data
        cur.execute(
            "SELECT dish_name, dish_description, dish_price "
            "FROM dishes "
            "WHERE dishes.dish_uuid = %s",
            [callback_data]
        )
        dish = cur.fetchone()
        cur.connection.close()
        return dish

    @logger_decorator
    def new_cart(self) -> None:
        """Create new cart in the DB.cart table and add Customer's Telegram ID in it.

        """
        cur = cursor()
        customer_id = self.input_object.from_user.id
        cur.execute("INSERT INTO cart (customer_id) VALUES (%s)", [customer_id])
        cur.connection.commit()
        cur.connection.close()

    @logger_decorator
    def add_to_cart(self, column_name: str) -> None:
        """Add required info into cart.

        Args:
            column_name: Name of column containing required info.

        """
        cur = cursor()
        callback_data = self.input_object.data
        customer_id = self.input_object.from_user.id
        cur.execute(
            "UPDATE cart "
            "SET " + column_name + " =%s "
            "WHERE cart.customer_id = %s",
            [
                callback_data,
                customer_id
            ]
        )
        cur.connection.commit()
        cur.connection.close()

    @logger_decorator
    def get_from_cart(self, column_name: str) -> float | int | str | List[Any] | None:
        """Get required info from cart.

        Args:
            column_name: Name of column containing required info.

        Returns:
            Required info.

        """
        cur = cursor()
        customer_id = self.input_object.from_user.id
        cur.execute("SELECT " + column_name + " FROM cart WHERE cart.customer_id = %s", [customer_id])
        value = cur.fetchone()
        return value[0] if value is not None else None

    @logger_decorator
    def delete_from_cart(self, column_name: str) -> None:
        """Delete required info from cart.

        Args:
            column_name: Name of column containing required info.

        """
        cur = cursor()
        customer_id = self.input_object.from_user.id
        cur.execute("UPDATE cart SET " + column_name + " =null WHERE cart.customer_id = %s", [customer_id])
        cur.connection.commit()
        cur.connection.close()

    @logger_decorator
    def delete_cart(self) -> None:
        """Delete cart connected to given Customer's Telegram ID.

        """
        cur = cursor()
        customer_id = self.input_object.from_user.id
        cur.execute("DELETE FROM cart WHERE cart.customer_id = %s", [customer_id])
        cur.connection.commit()
        cur.connection.close()

    @logger_decorator
    def check_if_location(self) -> Dict[str, float] | None:
        """Check if Customer's location is provided and return it if so.

        Returns:
            Customer's longitude and latitude if ones are provided.

        """
        cur = cursor()
        customer_id = self.input_object.from_user.id
        cur.execute(
            "SELECT customer_location "
            "FROM customers "
            "WHERE customers.customer_id = %s",
            [customer_id]
        )
        latlon = cur.fetchone()
        cur.connection.close()
        if latlon[0]:
            location = {
                "lat": latlon[0][0],
                "lon": latlon[0][1]
            }
            return location
