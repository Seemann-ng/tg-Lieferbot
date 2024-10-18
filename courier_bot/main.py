import telebot.types as types

import courier_menus
from courier_translations import texts
from courier_db_tools import Interface as DBInterface
from tools.bots_initialization import adm_bot, courier_bot, cus_bot, rest_bot
from tools.logger_tool import logger, logger_decorator_callback, logger_decorator_msg


@courier_bot.message_handler(commands=["start"])
@logger_decorator_msg
def start(message: types.Message) -> None:
    """Start interaction with bot;
    ask to send registration request to Admin,
    if User is not in courier database.

    Args:
        message: /start command message.

    """
    msg = DBInterface(message)
    lang_code = msg.get_courier_lang()
    user_id = msg.courier_id
    if not msg.courier_in_db():
        courier_bot.send_message(user_id, texts[lang_code]["ASK_REG_MSG"], reply_markup=types.ForceReply())
    else:
        courier_bot.send_message(user_id, texts[lang_code]["WELCOME_MSG"])


@courier_bot.message_handler(func=lambda message: message.reply_to_message \
                                                  and message.reply_to_message.text \
                                                  in [lang["ASK_REG_MSG"] for lang in texts.values()])
@logger_decorator_msg
def ask_registration(message: types.Message) -> None:
    """Process Courier registration request to Admin.

    Args:
        message: Courier registration request message.

    """
    msg = DBInterface(message)
    lang_code = msg.get_courier_lang()
    user_id = msg.courier_id
    user_name = msg.data_to_read.from_user.username
    admin_id = msg.get_support_id()
    adm_bot.send_message(admin_id, texts[lang_code]["REG_REQ_MSG"](user_name, user_id, message.text))
    courier_bot.send_message(user_id, texts[lang_code]["REG_REQ_SENT_MSG"])


@courier_bot.message_handler(commands=["select_language"])
@logger_decorator_msg
def change_lang_menu(message: types.Message) -> None:
    """Open language select menu.

    Args:
        message: Command with language select request.

    """
    msg = DBInterface(message)
    lang_code = msg.get_courier_lang()
    courier_id = msg.data_to_read.from_user.id
    courier_bot.send_message(courier_id, texts[lang_code]["LANG_SEL_MENU"])
    courier_bot.send_message(courier_id,
                             texts[lang_code]["CHANGE_LANG_MSG"],
                             reply_markup=courier_menus.lang_sel_menu(lang_code))


@courier_bot.callback_query_handler(func= lambda call: call.message.text \
                                                       in [lang["CHANGE_LANG_MSG"] for lang in texts.values()])
@logger_decorator_callback
def lang_set(call: types.CallbackQuery) -> None:
    """Change bot interface language.

    Args:
        call: Callback query with selected language info.

    """
    c_back = DBInterface(call)
    courier_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    c_back.set_courier_lang()
    courier_bot.delete_message(courier_id, message_id - 1)
    courier_bot.delete_message(courier_id, message_id)
    courier_bot.send_message(courier_id, texts[c_back.data_to_read.data]["LANG_SELECTED_MSG"])


@courier_bot.message_handler(commands=["open_shift"])
@logger_decorator_msg
def open_shift_command(message: types.Message) -> None:
    """Process request to open shift.

    Args:
        message: /open_shift command message.

    """
    msg = DBInterface(message)
    lang_code = msg.get_courier_lang()
    courier_id = msg.courier_id
    msg.open_shift()
    courier_bot.send_message(courier_id, texts[lang_code]["OPEN_SHIFT_MSG"])


@courier_bot.message_handler(commands=["close_shift"])
@logger_decorator_msg
def close_shift_command(message: types.Message) -> None:
    """Process request to close shift.

    Args:
        message: /close_shift command message.

    """
    msg = DBInterface(message)
    lang_code = msg.get_courier_lang()
    courier_id = msg.courier_id
    if msg.check_occupied():
        courier_bot.send_message(courier_id, texts[lang_code]["CANNOT_CLOSE_SHIFT_MSG"])
    else:
        msg.close_shift()
        courier_bot.send_message(courier_id, texts[lang_code]["CLOSE_SHIFT_MSG"])


@courier_bot.callback_query_handler(func=lambda call: "accept" in call.data)
@logger_decorator_callback
def accept_order(call: types.CallbackQuery) -> None:
    """Process request to accept order.

    Args:
        call: Callback query with request to accept order and order UUID.

    """
    c_back = DBInterface(call)
    order_uuid = c_back.data_to_read.data.split(maxsplit=1)[-1]
    message_id = c_back.data_to_read.message.id
    courier_lang = c_back.get_courier_lang()
    courier_id = c_back.data_to_read.from_user.id
    successful_acceptance = c_back.cur_accept_order()
    courier_bot.edit_message_reply_markup(courier_id, message_id)
    if successful_acceptance:
        courier_bot.edit_message_text(texts[courier_lang]["COUR_ORDER_ACCEPTED_MSG"](order_uuid),
                                      courier_id,
                                      message_id)
        customer_info = c_back.get_customer_info()
        customer_id = customer_info[0]
        customer_lang = customer_info[1]
        courier_info = c_back.get_courier_info()
        courier_name = courier_info[0]
        courier_username = courier_info[1]
        courier_phone = courier_info[2]
        cus_bot.send_message(customer_id,
                             texts[customer_lang]["COURIER_FOUND_MSG"](order_uuid,
                                                                       courier_name,
                                                                       courier_username,
                                                                       courier_phone))
        rest_info = c_back.get_rest_info()
        rest_id = rest_info[0]
        rest_lang = rest_info[1]
        rest_bot.send_message(rest_id,
                              texts[rest_lang]["COURIER_FOUND_MSG"](order_uuid,
                                                                    courier_name,
                                                                    courier_username,
                                                                    courier_phone))
        rest_bot.send_message(rest_id,
                              texts[rest_lang]["REST_ORDER_READY_MSG"](order_uuid),
                              reply_markup=courier_menus.rest_order_ready_menu(rest_lang, order_uuid))
    else:
        courier_bot.edit_message_text(texts[courier_lang]["ORDER_ALREADY_ACCEPTED_MSG"], courier_id, message_id)


@courier_bot.callback_query_handler(func=lambda call: "in_delivery" in call.data)
@logger_decorator_callback
def in_delivery(call: types.CallbackQuery) -> None:
    """Process confirmation from Courier that order has been received in delivery.

    Args:
        call: Callback query with confirmation and order UUID.

    """
    c_back = DBInterface(call)
    order_uuid = c_back.data_to_read.data.split(maxsplit=1)[-1]
    message_id = c_back.data_to_read.message.id
    courier_id = c_back.courier_id
    courier_lang = c_back.get_courier_lang()
    customer_info = c_back.get_customer_info()
    customer_id = customer_info[0]
    customer_lang = customer_info[1]
    c_back.order_in_delivery()
    courier_bot.edit_message_reply_markup(courier_id, message_id)
    courier_bot.send_message(courier_id,
                             texts[courier_lang]["COUR_IN_DELIVERY_MSG"](order_uuid),
                             reply_markup=courier_menus.order_in_delivery_menu(courier_lang, order_uuid))
    cus_bot.send_message(customer_id, texts[customer_lang]["CUS_IN_DELIVERY_MSG"](order_uuid))


@courier_bot.callback_query_handler(func=lambda call: "delivered" in call.data)
@logger_decorator_callback
def delivered(call: types.CallbackQuery) -> None:
    """Process confirmation from Courier that order has been delivered.

    Args:
        call: Callback query with confirmation and order UUID.

    """
    c_back = DBInterface(call)
    order_uuid = c_back.data_to_read.data.split(maxsplit=1)[-1]
    message_id = c_back.data_to_read.message.id
    courier_id = c_back.courier_id
    courier_lang = c_back.get_courier_lang()
    customer_info = c_back.get_customer_info()
    customer_id = customer_info[0]
    customer_lang = customer_info[1]
    c_back.order_delivered()
    courier_bot.edit_message_reply_markup(courier_id, message_id)
    courier_bot.send_message(courier_id, texts[courier_lang]["COUR_DELIVERED_MSG"](order_uuid))
    cus_bot.send_message(customer_id,
                         texts[customer_lang]["CUS_DELIVERED_MSG"](order_uuid),
                         reply_markup=courier_menus.cus_delivered_menu(customer_lang, order_uuid))


def main():
    logger.info("Bot is running")
    courier_bot.infinity_polling()


if __name__ == '__main__':
    main()
