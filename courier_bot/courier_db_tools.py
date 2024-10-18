import random
from typing import Tuple

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
        self.courier_id = data_to_read.from_user.id
        logger.info(f"Interface instance initialized with {type(self.data_to_read)}.")

    @cursor
    @logger_decorator
    def get_courier_lang(self, curs: psycopg2.extensions.cursor) -> str:
        """Get code of Courier's chosen language.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Code of Courier's chosen language
            if Courier has chosen one,
            otherwise default language code, set in .env.

        """
        courier_id = self.courier_id
        curs.execute("SELECT lang_code FROM couriers WHERE courier_id = %s", (courier_id,))
        if courier_lang := curs.fetchone():
            if courier_lang := courier_lang[0]:
                return courier_lang
        return DEF_LANG

    @cursor
    @logger_decorator
    def courier_in_db(self, curs: psycopg2.extensions.cursor) -> int:
        """Check if Courier is in database and get their Telegram ID if so.
        
        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Courier Telegram ID if Courier is in database,
            otherwise 0.
        """
        courier_id = self.courier_id
        curs.execute("SELECT courier_id FROM couriers WHERE courier_id = %s", (courier_id,))
        courier_id = curs.fetchone()
        return courier_id if courier_id else 0

    @cursor
    @logger_decorator
    def get_support_id(self, curs: psycopg2.extensions.cursor) -> int:
        """Get Telegram ID of ramdom Admin in the database.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Telegram ID of Admin.

        """
        curs.execute("SELECT admin_id FROM admins")
        if admin_ids := curs.fetchall():
            return random.choice(admin_ids)[0]

    @cursor
    @logger_decorator
    def set_courier_lang(self, curs: psycopg2.extensions.cursor) -> None:
        """Set new language code for Courier.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        lang_code = self.data_to_read.data
        courier_id = self.courier_id
        curs.execute("UPDATE couriers SET lang_code = %s WHERE courier_id = %s", (lang_code, courier_id))

    @cursor
    @logger_decorator
    def open_shift(self, curs: psycopg2.extensions.cursor) -> None:
        """Make Courier available to receive orders.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        courier_id = self.courier_id
        curs.execute("UPDATE couriers SET courier_status = true WHERE courier_id = %s", (courier_id,))

    @cursor
    @logger_decorator
    def check_occupied(self, curs: psycopg2.extensions.cursor) -> bool:
        """Check if Courier is currently delivering order.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            True if Courier is currently delivering order,
            False otherwise.

        """
        courier_id = self.courier_id
        curs.execute("SELECT is_occupied FROM couriers WHERE courier_id = %s", (courier_id,))
        occupation_status = curs.fetchone()[0]
        return occupation_status

    @cursor
    @logger_decorator
    def close_shift(self, curs: psycopg2.extensions.cursor) -> None:
        """Close Courier's shift and make them unavailable to receive orders.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        courier_id = self.courier_id
        curs.execute("UPDATE couriers SET courier_status = false WHERE courier_id = %s", (courier_id,))

    @cursor
    @logger_decorator
    def cur_accept_order(self, curs: psycopg2.extensions.cursor) -> bool:
        """Accept order by Courier,
        add info on Courier in order data in database,
        Check if order was accepted by Courier.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            True if order was accepted by Courier,
            False otherwise.

        """
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        courier_id = self.courier_id
        new_status = "'Preparing, courier found'"
        curs.execute("SELECT courier_legal_name FROM couriers WHERE courier_id = %s", (courier_id,))
        courier_name = curs.fetchone()[0]
        curs.execute("UPDATE orders SET courier_id = %s, courier_name = %s, order_status = %s "
                     "WHERE order_uuid = %s AND courier_id = -1",
                     (courier_id, courier_name, new_status, order_uuid))
        curs.execute("SELECT courier_id FROM orders WHERE order_uuid = %s", (order_uuid,))
        courier_id_db = curs.fetchone()[0]
        if courier_id == courier_id_db:
            curs.execute("UPDATE couriers SET is_occupied = true WHERE courier_id = %s ", (courier_id,))
        return courier_id_db == courier_id

    @cursor
    @logger_decorator
    def get_customer_info(self, curs: psycopg2.extensions.cursor) -> Tuple[int, str]:
        """Get information about Customer in database.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Array containing Customer Telegram ID and Customer language code.

        """
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("SELECT customer_id FROM orders WHERE order_uuid = %s", (order_uuid,))
        customer_id = curs.fetchone()[0]
        curs.execute("SELECT lang_code FROM customers WHERE customer_id = %s", (customer_id,))
        lang_code = curs.fetchone()[0]
        customer_info = (customer_id, lang_code)
        return customer_info

    @cursor
    @logger_decorator
    def get_courier_info(self, curs: psycopg2.extensions.cursor) -> Tuple[int, str]:
        """Get information about Courier in database.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Array containing Courier legal name, Telegram username and phone number.

        """
        courier_id = self.courier_id
        curs.execute("SELECT courier_legal_name, courier_username, courier_phone_num "
                     "FROM couriers WHERE courier_id = %s",
                     (courier_id,))
        courier_info = curs.fetchone()
        return courier_info

    @cursor
    @logger_decorator
    def get_rest_info(self, curs: psycopg2.extensions.cursor) -> Tuple[int, str]:
        """Get information about Restaurant in database.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Array containing Restaurant Telegram ID and Restaurant language code.

        """
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("SELECT restaurant_id FROM orders WHERE order_uuid = %s", (order_uuid,))
        restaurant_id = curs.fetchone()[0]
        curs.execute("SELECT lang_code FROM restaurants WHERE restaurant_tg_id = %s", (restaurant_id,))
        lang_code = curs.fetchone()[0]
        rest_info = (restaurant_id, lang_code)
        return rest_info

    @cursor
    @logger_decorator
    def order_in_delivery(self, curs: psycopg2.extensions.cursor) -> None:
        """Change order status to "In delivery".

        Args:
            curs: Cursor object from psycopg2 module.

        """
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("UPDATE orders SET order_status = 'In delivery' WHERE order_uuid = %s", (order_uuid,))

    @cursor
    @logger_decorator
    def order_delivered(self, curs: psycopg2.extensions.cursor) -> None:
        """Change order status to "Delivered".

        Args:
            curs: Cursor object from psycopg2 module.

        """
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("UPDATE orders SET order_status = 'Delivered' WHERE order_uuid = %s ",
                     (order_uuid,))
