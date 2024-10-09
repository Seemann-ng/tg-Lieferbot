import functools
import random
import uuid
from typing import Dict, List, Tuple, Any

import psycopg2
import telebot.types as types
from environs import Env

from logger_tool import logger, logger_decorator

env = Env()
env.read_env()

DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DEF_LANG = env.str("DEF_LANG", default="en_US")


def cursor(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(database="postgres",
                                user=DB_USER,
                                password=DB_PASSWORD,
                                host="liefer_bot_db",
                                port=5432)
        curs = conn.cursor()
        result = func(*args, **kwargs, curs=curs)
        conn.commit()
        conn.close()
        return result

    return wrapper


class Interface:
    def __init__(self, data_to_read: types.Message | types.CallbackQuery):
        self.data_to_read = data_to_read
        self.user_id = data_to_read.from_user.id
        logger.info(f"Interface instance initialized with {type(self.data_to_read)}.")

    @cursor
    @logger_decorator
    def get_rest_lang(self, curs: psycopg2.extensions.cursor) -> str:
        """Get code of Restaurant's chosen language.

        Args:
            curs: PostgreSQL cursor object.

        Returns:
            Code of Restaurant's chosen language
            if Restaurant has chosen one,
            otherwise default language code, set in .env.

        """
        user_id = self.user_id
        curs.execute("SELECT lang_code FROM restaurants WHERE restaurants.restaurant_tg_id = %s",
                     (user_id,))
        if user_lang := curs.fetchone():
            if customer_lang := user_lang[0]:
                return customer_lang
        return DEF_LANG

    @cursor
    @logger_decorator
    def rest_in_db(self, curs: psycopg2.extensions.cursor) -> bool:
        """

        Args:
            curs:

        Returns:

        """  # TODO
        curs.execute("SELECT restaurant_tg_id FROM restaurants")
        rest_ids = curs.fetchall()
        return self.user_id in [rest[0] for rest in rest_ids]

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
    def get_rest_uuid(self, curs: psycopg2.extensions.cursor) -> str:
        """

        Args:
            curs:

        Returns:

        """  # TODO
        user_id = self.user_id
        curs.execute("SELECT restaurant_uuid FROM restaurants WHERE restaurants.restaurant_tg_id = %s",
                     (user_id,))
        restaurant_uuid = curs.fetchone()
        return restaurant_uuid[0]

    @cursor
    @logger_decorator
    def get_dishes(self, curs: psycopg2.extensions.cursor) -> List[Tuple[Any, ...]]:
        """
        
        Args:
            curs: 

        Returns:

        """  # TODO
        rest_uuid = self.get_rest_uuid()
        curs.execute("SELECT dish_uuid, dish_name FROM dishes WHERE dishes.restaurant_uuid = %s",
                     (rest_uuid,))
        dishes = curs.fetchall()
        return dishes

    @cursor
    @logger_decorator
    def get_dish_name(self, curs: psycopg2.extensions.cursor) -> str | None:
        """
        
        Args:
            curs: 

        Returns:

        """  # TODO
        curs.execute("SELECT dish_name FROM dishes WHERE dishes.dish_uuid = %s",
                     (self.data_to_read.data,))
        if dish_name := curs.fetchone():
            return dish_name[0]

    @cursor
    @logger_decorator
    def add_dish(self, dish_name: str, curs: psycopg2.extensions.cursor) -> None:
        """

        Args:
            dish_name: 
            curs:

        Returns:

        """  # TODO
        curs.execute("INSERT INTO dishes(restaurant_uuid, dish_uuid, dish_name) VALUES (%s, %s, %s)",
                     (self.get_rest_uuid(), str(uuid.uuid4()), dish_name))

    # @cursor
    # @logger_decorator
    # def edit_dish(self, param: str, curs: psycopg2.extensions.cursor) -> None:  # TODO
    #     """
    #
    #     Args:
    #         param:
    #         curs:
    #
    #     Returns:
    #
    #     """
    #     curs.execute("UPDATE dishes SET " + param + " = %s WHERE dish_uuid = %s",
    #                  ())
