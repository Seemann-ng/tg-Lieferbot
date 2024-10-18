import uuid
import random
from typing import List, Tuple, Any

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
            if user_lang := user_lang[0]:
                return user_lang
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
    def set_restaurant_lang(self, curs: psycopg2.extensions.cursor) -> None:
        """
        
        Args:
            curs: 

        Returns:

        """  # TODO
        curs.execute("UPDATE restaurants SET lang_code = %s WHERE restaurants.restaurant_uuid = %s",
                     (self.data_to_read.data, self.get_rest_uuid()))

    @cursor
    @logger_decorator
    def open_shift(self, curs: psycopg2.extensions.cursor) -> None:
        """
        
        Args:
            curs: 

        Returns:

        """  # TODO
        curs.execute("UPDATE restaurants SET restaurant_is_open = true WHERE restaurant_tg_id = %s",
                     (self.user_id,))

    @cursor
    @logger_decorator
    def close_shift(self, curs: psycopg2.extensions.cursor) -> None:
        """

        Args:
            curs: 

        Returns:

        """  # TODO
        curs.execute("UPDATE restaurants SET restaurant_is_open = false WHERE restaurant_tg_id = %s",
                     (self.user_id,))

    @cursor
    @logger_decorator
    def set_dish_available(self, curs: psycopg2.extensions.cursor) -> None:
        """
        
        Args:
            curs: 

        Returns:

        """  # TODO
        curs.execute("UPDATE dishes SET dish_is_available = true WHERE dish_uuid = %s",
                     (self.data_to_read.data,))

    @cursor
    @logger_decorator
    def set_dish_unavailable(self, curs: psycopg2.extensions.cursor) -> None:
        """

        Args:
            curs: 

        Returns:

        """  # TODO
        curs.execute("UPDATE dishes SET dish_is_available = false WHERE dish_uuid = %s",
                     (self.data_to_read.data,))

    @cursor
    @logger_decorator
    def delete_dish(self, curs: psycopg2.extensions.cursor) -> None:
        """

        Args:
            curs:

        Returns:

        """  # TODO
        curs.execute("DELETE FROM dishes WHERE dish_uuid = %s", (self.data_to_read.data,))

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

    @cursor
    @logger_decorator
    def edit_dish(self, param: str, dish_uuid: str, curs: psycopg2.extensions.cursor) -> None:  # TODO
        """

        Args:
            param:
            dish_uuid:
            curs:

        Returns:

        """  # TODO
        curs.execute("UPDATE dishes SET " + param + " = %s WHERE dish_uuid = %s",
                     (self.data_to_read.text, dish_uuid))

    @cursor
    @logger_decorator
    def order_accepted(self, curs: psycopg2.extensions.cursor) -> None:
        """

        Args:
            curs:

        Returns:

        """  # TODO
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("UPDATE orders SET order_status = 'Accepted by res-t. Looking for courier.' "
                     "WHERE order_uuid = %s",
                     (order_uuid, ))

    @staticmethod
    @cursor
    @logger_decorator
    def get_available_couriers(curs: psycopg2.extensions.cursor) -> List[Tuple[Any, ...]]:
        """

        Args:
            curs:

        Returns:

        """  # TODO
        curs.execute("SELECT courier_id, lang_code FROM couriers WHERE courier_status = true AND is_occupied = false")
        couriers = curs.fetchall()
        return couriers if couriers else []

    @cursor
    @logger_decorator
    def get_customer(self, curs: psycopg2.extensions.cursor) -> Tuple[Any, ...]:
        """

        Args:
            curs:

        Returns:

        """  # TODO
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("SELECT customer_id FROM orders WHERE order_uuid = %s", (order_uuid, ))
        customer_id = curs.fetchone()[0]
        curs.execute("SELECT lang_code FROM customers WHERE customer_id = %s", (customer_id, ))
        lang_code = curs.fetchone()[0]
        customer = (customer_id, lang_code)
        return customer

    @cursor
    @logger_decorator
    def get_rest_location(self, curs: psycopg2.extensions.cursor) -> Tuple[str, List[int]]:
        """

        Args:
            curs:

        Returns:

        """  # TODO
        rest_id = self.user_id
        curs.execute("SELECT address, location FROM restaurants WHERE restaurant_tg_id = %s", (rest_id, ))
        location = curs.fetchone()
        return location

    @cursor
    @logger_decorator
    def get_delivery_location(self, curs: psycopg2.extensions.cursor) -> Tuple[List[int], ...]:
        """

        Args:
            curs:

        Returns:

        """  # TODO
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("SELECT delivery_location FROM orders WHERE order_uuid = %s", (order_uuid, ))
        delivery_location = curs.fetchone()
        return delivery_location

    @cursor
    @logger_decorator
    def get_order_items(self, curs: psycopg2.extensions.cursor) -> List[str]:
        """

        Args:
            curs:

        Returns:

        """  # TODO
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("SELECT dishes FROM orders WHERE order_uuid = %s", (order_uuid, ))
        dishes = curs.fetchone()[0]
        return dishes

    @cursor
    @logger_decorator
    def get_rest_name(self, curs: psycopg2.extensions.cursor) -> str:
        """

        Args:
            curs:

        Returns:

        """  # TODO
        curs.execute("SELECT restaurant_name FROM restaurants WHERE restaurant_tg_id = %s",
                     (self.user_id, ))
        rest_name = curs.fetchone()[0]
        return rest_name

    @cursor
    @logger_decorator
    def get_courier_fee(self, curs: psycopg2.extensions.cursor) -> float:
        """

        Args:
            curs:

        Returns:

        """  # TODO
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("SELECT courier_fee FROM orders WHERE order_uuid = %s", (order_uuid, ))
        courier_fee = curs.fetchone()[0]
        return courier_fee

    @cursor
    @logger_decorator
    def get_customer_info(self, curs: psycopg2.extensions.cursor) -> Tuple[str, ...]:
        """

        Args:
            curs:

        Returns:

        """  # TODO
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("SELECT customer_name, customer_id FROM orders WHERE order_uuid = %s", (order_uuid, ))
        customer_info = curs.fetchone()
        customer_name = customer_info[0]
        customer_id = customer_info[1]
        curs.execute("SELECT customer_username, customer_phone_num FROM customers WHERE customer_id = %s",
                     (customer_id, ))
        customer_info = curs.fetchone()
        customer_username = customer_info[0]
        customer_phone_num = customer_info[1]
        customer_info = (customer_name, customer_username, customer_phone_num)
        return customer_info

    @cursor
    @logger_decorator
    def get_courier(self, curs: psycopg2.extensions.cursor) -> Tuple[int, str]:
        """

        Args:
            curs:

        Returns:

        """  # TODO
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("SELECT courier_id FROM orders WHERE order_uuid = %s", (order_uuid, ))
        courier_id = curs.fetchone()[0]
        curs.execute("SELECT lang_code FROM couriers WHERE courier_id = %s", (courier_id, ))
        lang_code = curs.fetchone()[0]
        courier = (courier_id, lang_code)
        return courier

    @cursor
    @logger_decorator
    def order_ready(self, curs: psycopg2.extensions.cursor) -> None:
        """

        Args:
            curs:

        Returns:

        """  # TODO
        order_uuid = self.data_to_read.data.split(maxsplit=1)[-1]
        curs.execute("UPDATE orders SET order_status = 'Order ready, handled to the courier' "
                     "WHERE order_uuid = %s",
                     (order_uuid,))
        curs.execute("SELECT account_balance FROM restaurants WHERE restaurant_tg_id = %s",
                     (self.user_id,))
        current_balance = float(curs.fetchone()[0])
        curs.execute("SELECT dishes_subtotal FROM orders WHERE order_uuid = %s", (order_uuid,))
        to_be_added = float(curs.fetchone()[0])
        new_balance = round(current_balance + to_be_added, 2)
        curs.execute("UPDATE restaurants SET account_balance = %s WHERE restaurant_tg_id = %s ",
                     (new_balance, self.user_id))
