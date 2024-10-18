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
    def get_lang(self, curs: psycopg2.extensions.cursor) -> str:
        """Get Admin's lang code from the DB.

        Args:
            curs: Cursor object form psycopg2 module.

        Returns:
            Admin's lang code.

        """
        admin_id = self.data_to_read.from_user.id
        curs.execute("SELECT lang_code FROM admins WHERE admin_id = %s", (admin_id,))
        if lang_code := curs.fetchone():
            if lang_code := lang_code[0]:
                return lang_code
        return DEF_LANG

    @cursor
    @logger_decorator
    def get_from_orders(self, column: str, curs: psycopg2.extensions.cursor) -> str | int:
        """Get data about order from orders table in the DB.

        Args:
            column: Column name.
            curs: Cursor object form psycopg2 module.

        Returns:
            Required data.

        """
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("SELECT " + column + " FROM orders WHERE order_uuid = %s", (order_uuid,))
        order_info = curs.fetchone()[0]
        return order_info

    @cursor
    @logger_decorator
    def get_rest_lang(self, curs: psycopg2.extensions.cursor) -> str:
        """Get lang code of the Restaurant mentioned in the order from the DB.

        Args:
            curs: Cursor object form psycopg2 module.

        Returns:
            Restaurant's lang code.

        """
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("SELECT restaurant_uuid FROM orders WHERE order_uuid = %s", (order_uuid,))
        restaurant_uuid = curs.fetchone()[0]
        curs.execute("SELECT lang_code FROM restaurants WHERE restaurant_uuid = %s", (restaurant_uuid,))
        if lang_code := curs.fetchone():
            if lang_code := lang_code[0]:
                return lang_code
        return DEF_LANG

    @cursor
    @logger_decorator
    def update_order(self, column: str, new_value: str, curs: psycopg2.extensions.cursor) -> None:
        """Update order data in the DB.

        Args:
            column: Required column name.
            new_value: Required new value.
            curs: Cursor object form psycopg2 module.

        """
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("UPDATE orders SET " + column + " = %s WHERE order_uuid = %s", (new_value, order_uuid))

    @staticmethod
    @cursor
    @logger_decorator
    def get_customer_lang(customer_id: str, curs: psycopg2.extensions.cursor) -> str:
        """Get Customer lang code from the DB.

        Args:
            customer_id: Required Customer id.
            curs: Cursor object form psycopg2 module.

        Returns:
            Customer's lang code.

        """
        curs.execute("SELECT lang_code FROM customers WHERE customer_id = %s", (customer_id,))
        if lang_code := curs.fetchone():
            if lang_code := lang_code[0]:
                return lang_code
        return DEF_LANG
