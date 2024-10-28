import random
from typing import Tuple

import telebot.types as types
from environs import Env
from psycopg2.extensions import cursor

from tools.logger_tool import logger, logger_decorator
from tools.cursor_tool import cursor as cursor_decorator

env = Env()
env.read_env()

DEF_LANG = env.str("DEF_LANG", default="en_US")


class Interface:
    def __init__(self, data_to_read: types.Message | types.CallbackQuery):
        self.data_to_read = data_to_read
        self.courier_id = data_to_read.from_user.id
        logger.info(f"Interface instance initialized with {type(self.data_to_read)}.")

    @cursor_decorator
    @logger_decorator
    def get_courier_lang(self, curs: cursor) -> str:
        """Get code of Courier's chosen language.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Code of Courier's chosen language if Courier has chosen one,
            otherwise default language code, set in .env.

        """
        curs.execute("SELECT lang_code FROM couriers WHERE courier_id = %s", (self.courier_id,))
        lang = DEF_LANG
        if courier_lang := curs.fetchone():
            lang = courier_lang[0] or lang
        return lang

    @cursor_decorator
    @logger_decorator
    def courier_in_db(self, curs: cursor) -> int:
        """Check if Courier is in database and get their Telegram ID if
        so.
        
        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Courier Telegram ID if Courier is in database, otherwise 0.
        """
        curs.execute("SELECT courier_id FROM couriers WHERE courier_id = %s", (self.courier_id,))
        courier_id = 0 or curs.fetchone()
        return courier_id

    @cursor_decorator
    @logger_decorator
    def get_support_id(self, curs: cursor) -> int:
        """Get Telegram ID of ramdom Admin in the database.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Telegram ID of Admin.

        """
        curs.execute("SELECT admin_id FROM admins")
        if admin_ids := curs.fetchall():
            return random.choice(admin_ids)[0]

    @cursor_decorator
    @logger_decorator
    def set_courier_lang(self, curs: cursor) -> None:
        """Set new language code for Courier.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        curs.execute(
            "UPDATE couriers SET lang_code = %s WHERE courier_id = %s",
            (self.data_to_read.data, self.courier_id)
        )

    @cursor_decorator
    @logger_decorator
    def get_salary_balance(self, curs: cursor) -> float:
        """Get Courier's salary balance from the database.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Courier's salary balance.

        """
        curs.execute(
            "SELECT account_balance FROM couriers WHERE courier_id = %s",
            (self.courier_id,)
        )
        return float(curs.fetchone()[0])

    @cursor_decorator
    @logger_decorator
    def set_courier_type(self, curs: cursor) -> None:
        """Set Courier's type in the database. (0 - for foot, 1 - for
        bycycle, 2 - for motorcycle, 3 - for automobile)

        Args:
            curs: Cursor object from psycopg2 module.

        """
        curs.execute(
            "UPDATE couriers SET courier_type = %s WHERE courier_id = %s",
            (self.data_to_read.data.split(maxsplit=1)[-1], self.courier_id)
        )

    @cursor_decorator
    @logger_decorator
    def open_shift(self, curs: cursor) -> None:
        """Make Courier available to receive orders.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        curs.execute(
            "UPDATE couriers SET courier_status = true WHERE courier_id = %s",
            (self.courier_id,)
        )

    @cursor_decorator
    @logger_decorator
    def check_occupied(self, curs: cursor) -> bool:
        """Check if Courier is currently delivering order.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            True if Courier is currently delivering order, False
            otherwise.

        """
        curs.execute("SELECT is_occupied FROM couriers WHERE courier_id = %s", (self.courier_id,))
        return curs.fetchone()[0]

    @cursor_decorator
    @logger_decorator
    def close_shift(self, curs: cursor) -> None:
        """Close Courier's shift and make them unavailable to receive
        orders.

        Args:
            curs: Cursor object from psycopg2 module.

        """
        curs.execute(
            "UPDATE couriers SET courier_status = false WHERE courier_id = %s", (self.courier_id,)
        )

    @cursor_decorator
    @logger_decorator
    def cur_accept_order(self, curs: cursor) -> bool:
        """Accept order by Courier, add info on Courier in order data in
        database, Check if order was accepted by Courier.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            True if order was accepted by Courier, False otherwise.

        """
        curs.execute(
            "SELECT courier_legal_name FROM couriers WHERE courier_id = %s",
            (self.courier_id,)
        )
        courier_name = curs.fetchone()[0]
        curs.execute(
            "UPDATE orders SET courier_id = %s, courier_name = %s, order_status = '4' "
            "WHERE order_uuid = %s AND courier_id = -1",
            (self.courier_id, courier_name, self.data_to_read.data.split(maxsplit=1)[-1])
        )
        curs.execute(
            "SELECT courier_id FROM orders WHERE order_uuid = %s",
            (self.data_to_read.data.split(maxsplit=1)[-1],)
        )
        courier_id_db = curs.fetchone()[0]
        if self.courier_id == courier_id_db:
            curs.execute(
                "UPDATE couriers SET is_occupied = true WHERE courier_id = %s ", (self.courier_id,)
            )
        return courier_id_db == self.courier_id

    @cursor_decorator
    @logger_decorator
    def get_customer_info(self, curs: cursor) -> Tuple[int, str]:
        """Get information about Customer in database.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Array containing Customer Telegram ID and Customer language
            code.

        """
        curs.execute(
            "SELECT customer_id FROM orders WHERE order_uuid = %s",
            (self.data_to_read.data.split(maxsplit=1)[-1],)
        )
        customer_id = curs.fetchone()[0]
        curs.execute("SELECT lang_code FROM customers WHERE customer_id = %s", (customer_id,))
        customer_info = (customer_id, curs.fetchone()[0])
        return customer_info

    @cursor_decorator
    @logger_decorator
    def get_courier_info(self, curs: cursor) -> Tuple[int, str]:
        """Get information about Courier in database.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Array containing Courier legal name, Telegram username and
            phone number.

        """
        curs.execute(
            "SELECT courier_legal_name, courier_username, courier_phone_num FROM couriers "
            "WHERE courier_id = %s",
            (self.courier_id,)
        )
        return curs.fetchone()

    @cursor_decorator
    @logger_decorator
    def get_rest_info(self, curs: cursor) -> Tuple[int, str]:
        """Get information about Restaurant in database.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Array containing Restaurant Telegram ID and Restaurant
            language code.

        """
        curs.execute(
            "SELECT restaurant_id FROM orders WHERE order_uuid = %s",
            (self.data_to_read.data.split(maxsplit=1)[-1],)
        )
        restaurant_id = curs.fetchone()[0]
        curs.execute(
            "SELECT lang_code FROM restaurants WHERE restaurant_tg_id = %s",
            (restaurant_id,)
        )
        rest_info = (restaurant_id, curs.fetchone()[0])
        return rest_info

    @cursor_decorator
    @logger_decorator
    def order_in_delivery(self, curs: cursor) -> None:
        """Change order status to "In delivery".

        Args:
            curs: Cursor object from psycopg2 module.

        """
        curs.execute(
            "UPDATE orders SET order_status = '6' WHERE order_uuid = %s",
            (self.data_to_read.data.split(maxsplit=1)[-1],)
        )

    @cursor_decorator
    @logger_decorator
    def order_delivered(self, curs: cursor) -> None:
        """Change order status to "Delivered".

        Args:
            curs: Cursor object from psycopg2 module.

        """
        curs.execute(
            "UPDATE orders SET order_status = '7' WHERE order_uuid = %s ",
            (self.data_to_read.data.split(maxsplit=1)[-1],)
        )
