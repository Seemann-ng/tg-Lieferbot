import telebot.types as types

import admin_menus
from admin_translations import texts
from admin_db_tools import Interface as DBInterface
from tools.logger_tool import logger, logger_decorator_callback
from tools.bots_initialization import adm_bot, cus_bot, rest_bot


@adm_bot.callback_query_handler(func=lambda call: "confirmed" in call.data)
@logger_decorator_callback
def payment_confirmation(call: types.CallbackQuery) -> None:
    """Process payment confirmation by Admin.

    Args:
        call: Callback query with order UUID in it.

    """
    c_back = DBInterface(call)
    lang_code = c_back.get_lang()
    admin_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    order_uuid = c_back.data_to_read.data.split(maxsplit=1)[-1]
    dishes = c_back.get_from_orders("dishes")
    subtotal = c_back.get_from_orders("dishes_subtotal")
    restaurant_id = c_back.get_from_orders("restaurant_id")
    rest_lang_code = c_back.get_rest_lang()
    customer_id = c_back.get_from_orders("customer_id")
    customer_lang_code = c_back.get_customer_lang(customer_id)
    c_back.update_order("order_status", "Payment confirmed")
    adm_bot.edit_message_text(texts[lang_code]["PAYMENT_CONFIRMED_MSG"](order_uuid), admin_id, message_id)
    rest_bot.send_message(restaurant_id,
                          texts[rest_lang_code]["REST_NEW_ORDER_MSG"](order_uuid, dishes, subtotal),
                          reply_markup=admin_menus.rest_accept_order_menu(rest_lang_code, order_uuid))
    cus_bot.send_message(customer_id, texts[customer_lang_code]["CUS_PAYMENT_CONFIRMED_MSG"](order_uuid))


def main():
    logger.info("Bot is running")
    adm_bot.infinity_polling()


if __name__ == '__main__':
    main()
