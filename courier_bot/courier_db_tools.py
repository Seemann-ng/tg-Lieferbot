import random
# from typing import List, Tuple, Any

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
            curs: PostgreSQL cursor object.

        Returns:
            Code of Courier's chosen language
            if Courier has chosen one,
            otherwise default language code, set in .env.

        """
        courier_id = self.courier_id
        curs.execute("SELECT lang_code FROM couriers WHERE couriers.courier_id = %s",
                     (courier_id,))
        if courier_lang := curs.fetchone():
            if courier_lang := courier_lang[0]:
                return courier_lang
        return DEF_LANG

    @cursor
    @logger_decorator
    def courier_in_db(self, curs: psycopg2.extensions.cursor) -> int:
        """
        
        Args:
            curs: 

        Returns:

        """  # TODO
        curs.execute("SELECT courier_id FROM couriers")
        courier_id = curs.fetchone()
        return courier_id if courier_id else 0

    @cursor
    @logger_decorator
    def get_support_id(self, curs: psycopg2.extensions.cursor) -> int:
        """

        Args:
            curs:

        Returns:

        """  # TODO
        curs.execute("SELECT admin_id FROM admins")
        if admin_ids := curs.fetchall():
            return random.choice(admin_ids)[0]

    @cursor
    @logger_decorator
    def set_courier_lang(self, curs: psycopg2.extensions.cursor) -> None:
        """

        Args:
            curs: 

        Returns:

        """  # TODO
        curs.execute("UPDATE couriers SET lang_code = %s WHERE couriers.courier_id = %s",
                     (self.data_to_read.data, self.courier_id))

    @cursor
    @logger_decorator
    def open_shift(self, curs: psycopg2.extensions.cursor) -> None:
        """

        Args:
            curs: 

        Returns:

        """  # TODO
        curs.execute("UPDATE couriers SET courier_status = true WHERE courier_id = %s",
                     (self.courier_id, ))

    @cursor
    @logger_decorator
    def check_occupied(self, curs: psycopg2.extensions.cursor) -> bool:
        """

        Args:
            curs:

        Returns:

        """  # TODO
        curs.execute("SELECT is_occupied FROM couriers WHERE couriers.courier_id = %s",
                     (self.courier_id, ))
        occupation_status = curs.fetchone()[0]
        return occupation_status

    @cursor
    @logger_decorator
    def close_shift(self, curs: psycopg2.extensions.cursor) -> None:
        """

        Args:
            curs: 

        Returns:

        """  # TODO
        curs.execute("UPDATE couriers SET courier_status = false WHERE courier_id = %s",
                     (self.courier_id, ))
