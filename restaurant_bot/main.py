import telebot.types as types

import restaurant_menus
from restaurant_translations import texts
from restaurant_db_tools import Interface as DBInterface
from tools.bots_initialization import adm_bot, courier_bot, cus_bot, rest_bot
from tools.logger_tool import logger, logger_decorator_msg, logger_decorator_callback


@rest_bot.message_handler(commands=["start"])
@logger_decorator_msg
def start(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    if not msg.rest_in_db():
        rest_bot.send_message(user_id, texts[lang_code]["ASK_REGISTRATION_MSG"], reply_markup=types.ForceReply())
    else:
        rest_bot.send_message(user_id, texts[lang_code]["WELCOME_MSG"])


@rest_bot.message_handler(func=lambda message: message.reply_to_message \
                                               and message.reply_to_message.text \
                                               in [lang["ASK_REGISTRATION_MSG"] for lang in texts.values()])
@logger_decorator_msg
def ask_registration(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    user_name = msg.data_to_read.from_user.username
    admin_id = msg.get_support_id()
    adm_bot.send_message(admin_id, texts[lang_code]["REG_REQUEST_MSG"](user_name, user_id, message.text))
    rest_bot.send_message(user_id, texts[lang_code]["REG_REQUEST_SENT_MSG"])


@rest_bot.message_handler(commands=["select_language"])
@logger_decorator_msg
def change_lang_menu(message: types.Message) -> None:
    """Open language select menu.

    Args:
        message: Command with language select request.

    """
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.data_to_read.from_user.id
    rest_bot.send_message(user_id, texts[lang_code]["LANG_SEL_MENU"])
    rest_bot.send_message(user_id,
                          texts[lang_code]["CHANGE_LANG_MSG"],
                          reply_markup=restaurant_menus.lang_sel_menu(lang_code))


@rest_bot.callback_query_handler(func= lambda call: call.message.text \
                                                    in [lang["CHANGE_LANG_MSG"] for lang in texts.values()])
@logger_decorator_callback
def lang_set(call: types.CallbackQuery) -> None:
    """Change bot interface language.

    Args:
        call: Callback query with selected language info.

    """
    c_back = DBInterface(call)
    user_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    c_back.set_restaurant_lang()
    rest_bot.delete_message(user_id, message_id - 1)
    rest_bot.delete_message(user_id, message_id)
    rest_bot.send_message(user_id, texts[c_back.data_to_read.data]["LANG_SELECTED_MSG"])


@rest_bot.message_handler(commands=["dish_available"])
@logger_decorator_msg
def dish_available_command(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    rest_bot.send_message(user_id,
                          texts[lang_code]["DISH_AVAILABLE_SELECT_MSG"],
                          reply_markup=restaurant_menus.edit_dish_menu(lang_code, msg))


@rest_bot.callback_query_handler(func=lambda call: call.message.text \
                                                   in [lang["DISH_AVAILABLE_SELECT_MSG"] for lang in texts.values()])
@logger_decorator_callback
def dish_available_select(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    lang_code = c_back.get_rest_lang()
    user_id = c_back.user_id
    message_id = c_back.data_to_read.message.id
    c_back.set_dish_available()
    rest_bot.delete_message(user_id, message_id)
    rest_bot.send_message(user_id,
                          texts[lang_code]["DISH_SET_AVAILABLE_MSG"])


@rest_bot.message_handler(commands=["dish_unavailable"])
@logger_decorator_msg
def dish_unavailable_command(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    rest_bot.send_message(user_id,
                          texts[lang_code]["DISH_UNAVAILABLE_SELECT_MSG"],
                          reply_markup=restaurant_menus.edit_dish_menu(lang_code, msg))


@rest_bot.callback_query_handler(func=lambda call: call.message.text \
                                                   in [lang["DISH_UNAVAILABLE_SELECT_MSG"] for lang in texts.values()])
@logger_decorator_callback
def dish_unavailable_select(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    lang_code = c_back.get_rest_lang()
    user_id = c_back.user_id
    message_id = c_back.data_to_read.message.id
    rest_bot.delete_message(user_id, message_id)
    c_back.set_dish_unavailable()
    rest_bot.send_message(user_id,
                          texts[lang_code]["DISH_SET_UNAVAILABLE_MSG"])


@rest_bot.message_handler(commands=["add_dish"])
@logger_decorator_msg
def add_dish_command(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    if len(msg.data_to_read.text.split(maxsplit=1)) > 1:
        dish_name = msg.data_to_read.text.split(maxsplit=1)[1]
        msg.add_dish(dish_name)
        rest_bot.send_message(msg.user_id, texts[lang_code]["DISH_ADDED_MSG"](dish_name))
    else:
        rest_bot.send_message(msg.user_id, "No dish name found")


@rest_bot.message_handler(commands=["edit_dish"])
@logger_decorator_msg
def edit_dish_command(message: types.Message) -> None:
    """
    
    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    rest_bot.send_message(user_id,
                          texts[lang_code]["EDIT_DISH_MSG"],
                          reply_markup=restaurant_menus.edit_dish_menu(lang_code, msg))


@rest_bot.callback_query_handler(func=lambda call: call.message.text in [lang["EDIT_DISH_MSG"] for lang in texts.values()])
@logger_decorator_callback
def edit_dish_param(call: types.CallbackQuery) -> None:
    """
    
    Args:
        call: 

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    lang_code = c_back.get_rest_lang()
    user_id = c_back.user_id
    message_id = c_back.data_to_read.message.id
    if c_back.data_to_read.data == restaurant_menus.back_button(lang_code).callback_data:
        rest_bot.delete_message(user_id, message_id)
    else:
        rest_bot.edit_message_text(texts[lang_code]["EDIT_DISH_CHOSEN_MSG"](c_back.get_dish_name()), user_id, message_id)
        rest_bot.send_message(user_id,
                              texts[lang_code]["EDIT_DISH_PARAM_MSG"],
                              reply_markup=restaurant_menus.edit_dish_param_menu(lang_code, c_back))


@rest_bot.callback_query_handler(func=lambda call: call.message.text \
                                                   in [lang["EDIT_DISH_PARAM_MSG"] for lang in texts.values()])
@logger_decorator_callback
def req_new_dish_param(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    lang_code = c_back.get_rest_lang()
    user_id = c_back.user_id
    message_id = c_back.data_to_read.message.id
    rest_bot.delete_message(user_id, message_id - 1)
    rest_bot.delete_message(user_id, message_id)
    request = c_back.data_to_read.data.split(maxsplit=1)
    param_to_edit = request[0]
    dish_uuid = request[1]
    if c_back.data_to_read.data == restaurant_menus.back_button(lang_code):
        rest_bot.delete_message(user_id, message_id)
    elif param_to_edit == "cat":
        rest_bot.send_message(user_id, texts[lang_code]["EDIT_CATEGORY_MSG"](dish_uuid), reply_markup=types.ForceReply())
    elif param_to_edit == "des":
        rest_bot.send_message(user_id, texts[lang_code]["EDIT_DESCRIPTION_MSG"](dish_uuid), reply_markup=types.ForceReply())
    elif param_to_edit == "prc":
        rest_bot.send_message(user_id, texts[lang_code]["EDIT_PRICE_MSG"](dish_uuid), reply_markup=types.ForceReply())


@rest_bot.message_handler(func=lambda message: message.reply_to_message \
                                               and message.reply_to_message.text \
                                               in [lang["EDIT_CATEGORY_MSG"](message.reply_to_message.text.split()[-1])\
                                              for lang in texts.values()])
@logger_decorator_msg
def set_new_category(message: types.Message) -> None:
    """
    
    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    dish_uuid = message.reply_to_message.text.split()[-1]
    msg.edit_dish("category", dish_uuid)
    rest_bot.send_message(user_id, texts[lang_code]["CAT_SET_MSG"])


@rest_bot.message_handler(func=lambda message: message.reply_to_message \
                                               and message.reply_to_message.text \
                                               in [lang["EDIT_DESCRIPTION_MSG"](message.reply_to_message.text.split()[-1]) \
                                              for lang in texts.values()])
@logger_decorator_msg
def set_new_description(message: types.Message) -> None:
    """

    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    dish_uuid = message.reply_to_message.text.split()[-1]
    msg.edit_dish("dish_description", dish_uuid)
    rest_bot.send_message(user_id, texts[lang_code]["DESC_SET_MSG"])


@rest_bot.message_handler(func=lambda message: message.reply_to_message \
                                               and message.reply_to_message.text \
                                               in [lang["EDIT_PRICE_MSG"](message.reply_to_message.text.split()[-1]) \
                                              for lang in texts.values()])
@logger_decorator_msg
def set_new_price(message: types.Message) -> None:
    """

    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    dish_uuid = message.reply_to_message.text.split()[-1]
    msg.edit_dish("dish_price", dish_uuid)
    rest_bot.send_message(user_id, texts[lang_code]["PRICE_SET_MSG"])


@rest_bot.message_handler(commands=["delete_dish"])
@logger_decorator_msg
def delete_dish_command(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    rest_bot.send_message(user_id,
                          texts[lang_code]["DELETE_DISH_SELECT_MSG"],
                          reply_markup=restaurant_menus.edit_dish_menu(lang_code, msg))


@rest_bot.callback_query_handler(func=lambda call: call.message.text \
                                                   in [lang["DELETE_DISH_SELECT_MSG"] for lang in texts.values()])
@logger_decorator_callback
def dish_deletion_select(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    lang_code = c_back.get_rest_lang()
    user_id = c_back.user_id
    message_id = c_back.data_to_read.message.id
    rest_bot.delete_message(user_id, message_id)
    c_back.delete_dish()
    rest_bot.send_message(user_id,
                          texts[lang_code]["DISH_DELETED_MSG"])


@rest_bot.message_handler(commands=["close_shift"])
@logger_decorator_msg
def close_shift_command(message: types.Message) -> None:
    """

    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    msg.close_shift()
    rest_bot.send_message(user_id, texts[lang_code]["CLOSE_SHIFT_MSG"])


@rest_bot.message_handler(commands=["open_shift"])
@logger_decorator_msg
def open_shift_command(message: types.Message) -> None:
    """

    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    msg.open_shift()
    rest_bot.send_message(user_id, texts[lang_code]["OPEN_SHIFT_MSG"])


@rest_bot.callback_query_handler(func=lambda call: "accepted" in call.data)
@logger_decorator_callback
def order_accepted(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    message_id = c_back.data_to_read.message.id
    order_uuid = c_back.data_to_read.data.split(maxsplit=1)[-1]
    dishes = c_back.get_order_items()
    rest_name = c_back.get_rest_name()
    rest_lang_code = c_back.get_rest_lang()
    rest_id = c_back.user_id
    available_couriers = c_back.get_available_couriers()
    customer = c_back.get_customer()
    customer_id = customer[0]
    customer_lang = customer[1]
    customer_info = c_back.get_customer_info()
    customer_name = customer_info[0]
    customer_username = customer_info[1]
    customer_phone = customer_info[2]
    c_back.order_accepted()
    courier_fee = c_back.get_courier_fee()
    rest_location = c_back.get_rest_location()
    rest_address = rest_location[0]
    rest_lat = rest_location[1][0]
    rest_lon = rest_location[1][1]
    delivery_location = c_back.get_delivery_location()
    delivery_lat = delivery_location[0][0]
    delivery_lon = delivery_location[0][1]
    rest_bot.edit_message_reply_markup(rest_id, message_id)
    rest_bot.send_message(rest_id, texts[rest_lang_code]["REST_ORDER_ACCEPTED_MSG"](order_uuid))
    cus_bot.send_message(customer_id, texts[customer_lang]["CUST_ORDER_ACCEPTED_MSG"](order_uuid))
    for courier in available_couriers:
        courier_id = courier[0]
        courier_lang = courier[1]
        courier_bot.send_message(courier_id,
                                 texts[courier_lang]["LOOKING_FOR_COURIER_MSG"](order_uuid,
                                                                                courier_fee,
                                                                                customer_name,
                                                                                customer_username,
                                                                                customer_phone,
                                                                                rest_name,
                                                                                dishes,
                                                                                rest_address))
        courier_bot.send_location(courier_id, rest_lat, rest_lon)
        courier_bot.send_message(courier_id, texts[courier_lang]["COURIER_DELIVERY_LOC_MSG"])
        courier_bot.send_location(courier_id, delivery_lat, delivery_lon)
        courier_bot.send_message(courier_id,
                                 texts[courier_lang]["COURIER_ACCEPT_ORDER_MSG"],
                                 reply_markup=restaurant_menus.courier_accept_menu(order_uuid, courier_lang))


def main():
    logger.info("The bot is running.")
    rest_bot.infinity_polling()


if __name__ == "__main__":
    main()
