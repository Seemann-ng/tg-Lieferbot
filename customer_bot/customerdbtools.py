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


conn = psycopg2.connect(
    database=DB,
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = conn.cursor()


class DBInterface:
    @staticmethod
    def user_in_db(message: types.Message) -> str | None:
        """Check if Customer is in the DB and if so get their name or Telegram username.

        Args:
            message: Message from Customer.

        Returns:
            Customer name from the DB if Customer is in the DB and has provided their name,
            Telegram username if Customer is in the DB and has NOT provided their name,
            None if Customer is not in the DB.

        """
        cursor.execute(
            "SELECT customer_name, customer_username FROM customers WHERE customers.customer_id = %s",
            (message.from_user.id,)
        )
        customer_names = cursor.fetchone()
        if customer_names:
            if customer_names[0]:
                return customer_names[0]
            return customer_names[1]
        return None

    @classmethod
    def add_customer(cls, message: types.Message) -> None:
        """

        Args:
            message:

        Returns:

        """
        if not cls.user_in_db(message):
            cursor.execute(
                "INSERT INTO customers (customer_id, customer_username) VALUES (%s, %s)",
                (message.from_user.id, message.from_user.username)
            )
            conn.commit()

    @staticmethod
    def update_name(message: types.Message) -> None:
        """

        Args:
            message:

        Returns:

        """
        cursor.execute(
            "UPDATE customers SET customer_name = %s WHERE customers.customer_id = %s",
            (message.text, message.from_user.id)
        )
        conn.commit()

    @staticmethod
    def update_phone_number(customer_id: int, phone_number: str) -> None:
        """

        Args:
            customer_id:
            phone_number:

        Returns:

        """
        cursor.execute(
            "UPDATE customers SET customer_phone_num = %s WHERE customers.customer_id = %s",
            (phone_number, customer_id)
        )
        conn.commit()

    @staticmethod
    def update_customer_location(lat: float, lon: float, message: types.Message) -> None:
        cursor.execute(
            "UPDATE customers SET customer_latlon = '{%s, %s}' WHERE customers.customer_id = %s",
            (lat, lon, message.from_user.id)
        )
        conn.commit()

    @staticmethod
    def delete_customer(message: types.Message) -> None:
        cursor.execute(
            "DELETE FROM customers WHERE customers.customer_id = %s",
            (message.from_user.id,)
        )
