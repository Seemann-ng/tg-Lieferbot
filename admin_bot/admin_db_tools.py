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
        """

        Args:
            curs:

        Returns:

        """
        curs.execute("SELECT lang_code FROM admins WHERE admin_id = %s",
                     (self.data_to_read.from_user.id, ))
        lang_code = curs.fetchone()[0]
        return lang_code

    @cursor
    @logger_decorator
    def get_from_orders(self, column: str, curs: psycopg2.extensions.cursor) -> str | int:
        """

        Args:
            column:
            curs:

        Returns:

        """
        curs.execute("SELECT " + column + " FROM orders WHERE orders.order_uuid = %s",
                     (self.data_to_read.data.split(maxsplit=1)[1], ))
        order_info = curs.fetchone()[0]
        return order_info

    @cursor
    @logger_decorator
    def get_rest_lang(self, curs: psycopg2.extensions.cursor) -> str:
        """

        Args:
            curs:

        Returns:

        """
        curs.execute("SELECT restaurant_uuid FROM orders WHERE order_uuid = %s",
                     (self.data_to_read.data.split(maxsplit=1)[1], ))
        restaurant_uuid = curs.fetchone()[0]
        curs.execute("SELECT lang_code FROM restaurants WHERE restaurant_uuid = %s", (restaurant_uuid, ))
        if lang_code := curs.fetchone():
            if lang_code := lang_code[0]:
                return lang_code
        return DEF_LANG

    @cursor
    @logger_decorator
    def update_order(self, column: str, new_value: str, curs: psycopg2.extensions.cursor) -> None:
        """

        Args:
            column:
            new_value:
            curs:

        Returns:

        """
        curs.execute("UPDATE orders SET " + column + " = %s WHERE orders.order_uuid = %s",
                     (new_value, self.data_to_read.data.split(maxsplit=1)[1]))

    @staticmethod
    @cursor
    @logger_decorator
    def get_customer_lang(customer_id: str, curs: psycopg2.extensions.cursor) -> str:
        """

        Args:
            customer_id:
            curs:

        Returns:

        """
        curs.execute("SELECT lang_code FROM customers WHERE customer_id = %s", (customer_id, ))
        if lang_code := curs.fetchone():
            if lang_code := lang_code[0]:
                return lang_code
        return DEF_LANG
