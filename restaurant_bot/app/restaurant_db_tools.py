import uuid
import random
from typing import List, Tuple, Any

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
        self.user_id = data_to_read.from_user.id
        logger.info(f"Interface instance initialized with {type(self.data_to_read)}.")

    @cursor_decorator
    @logger_decorator
    def get_rest_lang(self, curs: cursor) -> str:
        """Get code of Restaurant's chosen language.

        Args:
            curs: Cursor object from psycopg2.

        Returns:
            Code of Restaurant's chosen language if Restaurant has
            chosen one, otherwise default language code, set in .env.

        """
        curs.execute(
            "SELECT lang_code FROM restaurants WHERE restaurant_tg_id = %s", (self.user_id,)
        )
        lang = DEF_LANG
        if user_lang := curs.fetchone():
            lang = user_lang[0] or lang
        return lang

    @cursor_decorator
    @logger_decorator
    def rest_in_db(self, curs: cursor) -> bool:
        """Check if Restaurant is in database.

        Args:
            curs: Cursor object from psycopg2.

        Returns:
            True if Restaurant is in database, otherwise False.

        """
        curs.execute("SELECT restaurant_tg_id FROM restaurants")
        rest_ids = curs.fetchall()
        return self.user_id in [rest[0] for rest in rest_ids]

    @cursor_decorator
    @logger_decorator
    def get_support_id(self, curs: cursor) -> int:
        """Get random Admin Telegram ID from database.

        Args:
            curs: Cursor object from psycopg2.

        Returns:
            Admin Telegram ID.

        """
        curs.execute("SELECT admin_id FROM admins")
        if admin_ids := curs.fetchall():
            return random.choice(admin_ids)[0]

    @cursor_decorator
    @logger_decorator
    def get_rest_uuid(self, curs: cursor) -> str:
        """Get Restaurant UUID from database.

        Args:
            curs: Cursor object from psycopg2.

        Returns:
            Restaurant UUID.

        """
        curs.execute(
            "SELECT restaurant_uuid FROM restaurants WHERE restaurant_tg_id = %s", (self.user_id,)
        )
        return curs.fetchone()[0]

    @cursor_decorator
    @logger_decorator
    def set_restaurant_lang(self, curs: cursor) -> None:
        """Set new language code for Restaurant.
        
        Args:
            curs: Cursor object from psycopg2.

        """
        curs.execute(
            "UPDATE restaurants SET lang_code = %s WHERE restaurant_uuid = %s",
            (self.data_to_read.data, self.get_rest_uuid())
        )

    @cursor_decorator
    @logger_decorator
    def open_shift(self, curs: cursor) -> None:
        """Mark Restaurant in database as Open.
        
        Args:
            curs: Cursor object from psycopg2.

        """
        curs.execute(
            "UPDATE restaurants SET restaurant_is_open = true WHERE restaurant_tg_id = %s",
            (self.user_id,)
        )

    @cursor_decorator
    @logger_decorator
    def close_shift(self, curs: cursor) -> None:
        """Mark Restaurant in database as Closed.

        Args:
            curs: Cursor object from psycopg2.

        """
        curs.execute(
            "UPDATE restaurants SET restaurant_is_open = false WHERE restaurant_tg_id = %s",
            (self.user_id,)
        )

    @cursor_decorator
    @logger_decorator
    def set_dish_available(self, curs: cursor) -> None:
        """Mark dish as available in database.
        
        Args:
            curs: Cursor object from psycopg2.

        """
        curs.execute(
            "UPDATE dishes SET dish_is_available = true WHERE dish_uuid = %s",
            (self.data_to_read.data,)
        )

    @cursor_decorator
    @logger_decorator
    def set_dish_unavailable(self, curs: cursor) -> None:
        """Mark dish as unavailable in database.

        Args:
            curs: Cursor object from psycopg2.

        """
        curs.execute(
            "UPDATE dishes SET dish_is_available = false WHERE dish_uuid = %s",
            (self.data_to_read.data,)
        )

    @cursor_decorator
    @logger_decorator
    def delete_dish(self, curs: cursor) -> None:
        """Delete dish from database.

        Args:
            curs: Cursor object from psycopg2.

        """
        curs.execute("DELETE FROM dishes WHERE dish_uuid = %s", (self.data_to_read.data,))

    @cursor_decorator
    @logger_decorator
    def get_dishes(self, curs: cursor) -> List[Tuple[Any, ...]]:
        """Get dishes of Restaurant from database.
        
        Args:
            curs: Cursor object from psycopg2.

        Returns:
            Array containing dish UUIDs and names.

        """
        curs.execute(
            "SELECT dish_uuid, dish_name FROM dishes WHERE restaurant_uuid = %s",
            (self.get_rest_uuid(),)
        )
        return curs.fetchall()

    @cursor_decorator
    @logger_decorator
    def get_dish_name(self, curs: cursor) -> str:
        """Get dish name from database by its UUID.
        
        Args:
            curs: Cursor object from psycopg2.

        Returns:
            Dish name.

        """
        curs.execute(
            "SELECT dish_name FROM dishes WHERE dish_uuid = %s", (self.data_to_read.data,)
        )
        if dish_name := curs.fetchone():
            return dish_name[0]

    @cursor_decorator
    @logger_decorator
    def add_dish(self, dish_name: str, curs: cursor) -> None:
        """Add dish to database.

        Args:
            dish_name: Dish name.
            curs: Cursor object from psycopg2.

        """
        curs.execute(
            "INSERT INTO dishes(restaurant_uuid, dish_uuid, dish_name) VALUES (%s, %s, %s)",
            (self.get_rest_uuid(), str(uuid.uuid4()), dish_name)
        )

    @cursor_decorator
    @logger_decorator
    def edit_dish(self, param: str, dish_uuid: str, curs: cursor) -> None:
        """Edit selected parameter of selected dish in database.

        Args:
            param: Name of parameter.
            dish_uuid: Dish UUID.
            curs: Cursor object from psycopg2.

        """
        curs.execute(
            "UPDATE dishes SET " + param + " = %s WHERE dish_uuid = %s",
            (self.data_to_read.text, dish_uuid)
        )

    @cursor_decorator
    @logger_decorator
    def order_accepted(self, curs: cursor) -> None:
        """Mark order as "accepted by restaurant" in database.

        Args:
            curs: Cursor object from psycopg2.

        """
        curs.execute(
            "UPDATE orders SET order_status = '3' WHERE order_uuid = %s",
            (self.data_to_read.data.split(maxsplit=1)[-1],)
        )

    @cursor_decorator
    @logger_decorator
    def get_available_couriers(self, curs: cursor) -> List[Tuple[Any, ...]]:
        """Get list of available couriers from database considering
        courier types and current order delivery distance.

        Args:
            curs: Cursor object from psycopg2.

        Returns:
            Array containing courier Telegram ID, lang codes and courier
            types of available couriers.

        """
        curs.execute(
            "SELECT courier_id, lang_code, courier_type FROM couriers "
            "WHERE courier_status = true AND is_occupied = false"
        )
        couriers = curs.fetchall()
        curs.execute(
            "SELECT delivery_distance FROM orders WHERE order_uuid = %s",
            (self.data_to_read.data.split(maxsplit=1)[-1],)
        )
        delivery_distance = float(curs.fetchone()[0])  # TODO remake algorithm.
        for courier in couriers:
            if courier[2] == "0" and delivery_distance >= 3:
                couriers.remove(courier)
            if courier[2] == "1" and delivery_distance >= 7:
                couriers.remove(courier)
            if courier[2] == "2" and delivery_distance >= 15:
                couriers.remove(courier)
        return couriers if couriers else []

    @cursor_decorator
    @logger_decorator
    def get_customer(self, curs: cursor) -> Tuple[Any, ...]:
        """Get info about customer from database.

        Args:
            curs: Cursor object from psycopg2.

        Returns:
            Array containing customer Telegram ID and lang code.

        """
        curs.execute(
            "SELECT customer_id FROM orders WHERE order_uuid = %s",
            (self.data_to_read.data.split(maxsplit=1)[-1],)
        )
        customer_id = curs.fetchone()[0]
        curs.execute("SELECT lang_code FROM customers WHERE customer_id = %s", (customer_id,))
        customer = (customer_id, curs.fetchone()[0])
        return customer

    @cursor_decorator
    @logger_decorator
    def get_rest_location(self, curs: cursor) -> Tuple[str, List[int]]:
        """Get info about restaurant location from database.

        Args:
            curs: Cursor object from psycopg2.

        Returns:
            Array containing restaurant address, and coordinates.

        """
        curs.execute(
            "SELECT address, location FROM restaurants WHERE restaurant_tg_id = %s",
            (self.user_id,)
        )
        return curs.fetchone()

    @cursor_decorator
    @logger_decorator
    def get_delivery_location(self, curs: cursor) -> Tuple[List[int], ...]:
        """Get delivery location from database.

        Args:
            curs: Cursor object from psycopg2.

        Returns:
            Array containing customer's latitude and longitude.

        """
        curs.execute(
            "SELECT delivery_location FROM orders WHERE order_uuid = %s",
            (self.data_to_read.data.split(maxsplit=1)[-1],)
        )
        return curs.fetchone()

    @cursor_decorator
    @logger_decorator
    def get_order_items(self, curs: cursor) -> List[str]:
        """Get order items names from database.

        Args:
            curs: Cursor object from psycopg2.

        Returns:
            Array containing order items names.

        """
        curs.execute(
            "SELECT dishes FROM orders WHERE order_uuid = %s",
            (self.data_to_read.data.split(maxsplit=1)[-1],)
        )
        return curs.fetchone()[0]

    @cursor_decorator
    @logger_decorator
    def get_rest_name(self, curs: cursor) -> str:
        """Get restaurant name from database by its Telegram ID.

        Args:
            curs: Cursor object from psycopg2.

        Returns:
            Restaurant name.

        """
        curs.execute(
            "SELECT restaurant_name FROM restaurants WHERE restaurant_tg_id = %s", (self.user_id,)
        )
        return curs.fetchone()[0]

    @cursor_decorator
    @logger_decorator
    def get_courier_fee(self, curs: cursor) -> float:
        """Get courier fee for current order from database.

        Args:
            curs: Cursor object from psycopg2.

        Returns:
            Courier fee.

        """
        curs.execute(
            "SELECT courier_fee FROM orders WHERE order_uuid = %s",
            (self.data_to_read.data.split(maxsplit=1)[-1],)
        )
        return curs.fetchone()[0]

    @cursor_decorator
    @logger_decorator
    def get_customer_info(self, curs: cursor) -> Tuple[str, ...]:
        """Get info about customer that created current order from
        database.

        Args:
            curs: Cursor object from psycopg2.

        Returns:
            Array containing customer name, Telegram username, phone
            number and order comment.

        """
        curs.execute(
            "SELECT customer_name, customer_id, order_comment FROM orders WHERE order_uuid = %s",
            (self.data_to_read.data.split(maxsplit=1)[-1],)
        )
        customer_info = curs.fetchone()
        curs.execute(
            "SELECT customer_username, customer_phone_num FROM customers WHERE customer_id = %s",
            (customer_info[1],)
        )
        customer_information = curs.fetchone()
        customer_info = (
            customer_info[0],
            customer_information[0],
            customer_information[1],
            customer_info[2]
        )
        return customer_info

    @cursor_decorator
    @logger_decorator
    def get_courier(self, curs: cursor) -> Tuple[int, str]:
        """Get information about courier from database.

        Args:
            curs: Cursor object from psycopg2.

        Returns:
            Array containing courier telegram ID and lang code.

        """
        curs.execute(
            "SELECT courier_id FROM orders WHERE order_uuid = %s",
            (self.data_to_read.data.split(maxsplit=1)[-1],)
        )
        courier_id = curs.fetchone()[0]
        curs.execute("SELECT lang_code FROM couriers WHERE courier_id = %s", (courier_id,))
        courier = (courier_id, curs.fetchone()[0])
        return courier

    @cursor_decorator
    @logger_decorator
    def order_ready(self, curs: cursor) -> None:
        """Set status "Order ready, handled over to a Courier" for order
        in database.

        Args:
            curs: Cursor object from psycopg2.

        """
        curs.execute(
            "UPDATE orders SET order_status = '5' WHERE order_uuid = %s",
            (self.data_to_read.data.split(maxsplit=1)[-1],)
        )
