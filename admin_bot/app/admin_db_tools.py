from typing import Any, Dict, List, Tuple

import telebot.types as types
from environs import Env
from psycopg2.extensions import cursor

from tools.cursor_tool import cursor as cursor_decorator
from tools.logger_tool import logger, logger_decorator

env = Env()
env.read_env()

DEF_LANG = env.str("DEF_LANG", default="en_US")

class Interface:
    def __init__(self, data_to_read: types.Message | types.CallbackQuery):
        self.data_to_read = data_to_read
        logger.info(f"Interface instance initialized with {type(self.data_to_read)}.")

    @cursor_decorator
    @logger_decorator
    def is_admin(self, curs: cursor) -> str:
        """Check if user is Admin.

        Args:
            curs: Cursor object from psycopg2.

        Returns:
            Admin Telegram username if the user is Admin, empty string
            otherwise.

        """
        curs.execute(
            "SELECT admin_username FROM admins WHERE admin_id = %s",
            (self.data_to_read.from_user.id,)
        )
        admin = "" or curs.fetchone()
        if admin:
            return admin[0]
        return admin

    @cursor_decorator
    @logger_decorator
    def get_admin_lang(self, curs: cursor) -> str:
        """Get code of Admins's chosen language.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Code of Admins's chosen language if Admin has chosen
            one, otherwise default language code, set in .env.

        """
        curs.execute(
            "SELECT lang_code FROM admins WHERE admin_id = %s",
            (self.data_to_read.from_user.id,)
        )
        lang = DEF_LANG
        if adm_lang := curs.fetchone():
            lang = adm_lang[0] or lang
        return lang

    @staticmethod
    @cursor_decorator
    @logger_decorator
    def get_couriers(curs: cursor) -> List[Tuple[Any, ...]]:
        """Get payment info about couriers from database.

        Args:
            curs: Cursor object from psycopg2 module.

        Returns:
            Array containing couriers Telegram IDs, Names, current
            balance, PayPal IDs and language codes.

        """
        curs.execute(
            "SELECT courier_id, courier_username, courier_legal_name, account_balance, paypal_id, "
            "lang_code FROM couriers WHERE account_balance != 0.00"
        )
        couriers = curs.fetchall()
        return couriers
