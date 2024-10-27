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
    if not msg.rest_in_db():
        rest_bot.send_message(
            msg.user_id,
            texts[msg.get_rest_lang()]["ASK_REGISTRATION_MSG"],
            reply_markup=types.ForceReply()
        )
    else:
        rest_bot.send_message(msg.user_id, texts[msg.get_rest_lang()]["WELCOME_MSG"])


@rest_bot.message_handler(
    func=lambda message: message.reply_to_message \
                         and message.reply_to_message.text \
                         in [lang["ASK_REGISTRATION_MSG"] for lang in texts.values()]
)
@logger_decorator_msg
def ask_registration(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    adm_bot.send_message(
        msg.get_support_id(),
        texts[msg.get_rest_lang()]["REG_REQUEST_MSG"](
            msg.data_to_read.from_user.username,
            msg.user_id,
            message.text
        )
    )
    rest_bot.send_message(msg.user_id, texts[msg.get_rest_lang()]["REG_REQUEST_SENT_MSG"])


@rest_bot.message_handler(commands=["select_language"])
@logger_decorator_msg
def change_lang_menu(message: types.Message) -> None:
    """Open language select menu.

    Args:
        message: Command with language select request.

    """
    msg = DBInterface(message)
    rest_bot.send_message(msg.user_id, texts[msg.get_rest_lang()]["LANG_SEL_MENU"])
    rest_bot.send_message(
        msg.user_id,
        texts[msg.get_rest_lang()]["CHANGE_LANG_MSG"],
        reply_markup=restaurant_menus.lang_sel_menu(msg.get_rest_lang())
    )


@rest_bot.callback_query_handler(
    func= lambda call: call.message.text in [lang["CHANGE_LANG_MSG"] for lang in texts.values()]
)
@logger_decorator_callback
def lang_set(call: types.CallbackQuery) -> None:
    """Change bot interface language.

    Args:
        call: Callback query with selected language info.

    """
    c_back = DBInterface(call)
    c_back.set_restaurant_lang()
    rest_bot.delete_message(c_back.data_to_read.from_user.id, (c_back.data_to_read.message.id - 1))
    rest_bot.delete_message(c_back.data_to_read.from_user.id, c_back.data_to_read.message.id)
    rest_bot.send_message(
        c_back.data_to_read.from_user.id,
        texts[c_back.data_to_read.data]["LANG_SELECTED_MSG"]
    )


@rest_bot.message_handler(commands=["dish_available"])
@logger_decorator_msg
def dish_available_command(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    rest_bot.send_message(
        msg.user_id,
        texts[msg.get_rest_lang()]["DISH_AVAILABLE_SELECT_MSG"],
        reply_markup=restaurant_menus.edit_dish_menu(msg.get_rest_lang(), msg)
    )


@rest_bot.callback_query_handler(
    func=lambda call: call.message.text \
                      in [lang["DISH_AVAILABLE_SELECT_MSG"] for lang in texts.values()]
)
@logger_decorator_callback
def dish_available_select(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    c_back.set_dish_available()
    rest_bot.delete_message(c_back.user_id, c_back.data_to_read.message.id)
    rest_bot.send_message(c_back.user_id, texts[c_back.get_rest_lang()]["DISH_SET_AVAILABLE_MSG"])


@rest_bot.message_handler(commands=["dish_unavailable"])
@logger_decorator_msg
def dish_unavailable_command(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    rest_bot.send_message(
        msg.user_id,
        texts[msg.get_rest_lang()]["DISH_UNAVAILABLE_SELECT_MSG"],
        reply_markup=restaurant_menus.edit_dish_menu(msg.get_rest_lang(), msg)
    )


@rest_bot.callback_query_handler(
    func=lambda call: call.message.text \
                      in [lang["DISH_UNAVAILABLE_SELECT_MSG"] for lang in texts.values()]
)
@logger_decorator_callback
def dish_unavailable_select(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    rest_bot.delete_message(c_back.user_id, c_back.data_to_read.message.id)
    c_back.set_dish_unavailable()
    rest_bot.send_message(
        c_back.user_id,
        texts[c_back.get_rest_lang()]["DISH_SET_UNAVAILABLE_MSG"]
    )


@rest_bot.message_handler(commands=["add_dish"])
@logger_decorator_msg
def add_dish_command(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    if len(msg.data_to_read.text.split(maxsplit=1)) > 1:
        msg.add_dish(msg.data_to_read.text.split(maxsplit=1)[-1])
        rest_bot.send_message(
            msg.user_id,
            texts[msg.get_rest_lang()]["DISH_ADDED_MSG"](
                msg.data_to_read.text.split(maxsplit=1)[-1]
            )
        )
    else:
        rest_bot.send_message(msg.user_id, texts[msg.get_rest_lang()]["NO_DISH_NAME_MSG"])


@rest_bot.message_handler(commands=["edit_dish"])
@logger_decorator_msg
def edit_dish_command(message: types.Message) -> None:
    """
    
    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    rest_bot.send_message(
        msg.user_id,
        texts[msg.get_rest_lang()]["EDIT_DISH_MSG"],
        reply_markup=restaurant_menus.edit_dish_menu(msg.get_rest_lang(), msg)
    )


@rest_bot.callback_query_handler(
    func=lambda call: call.message.text in [lang["EDIT_DISH_MSG"] for lang in texts.values()]
)
@logger_decorator_callback
def edit_dish_param(call: types.CallbackQuery) -> None:
    """
    
    Args:
        call: 

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    if c_back.data_to_read.data == restaurant_menus.back_button(
            c_back.get_rest_lang()
    ).callback_data:
        rest_bot.delete_message(c_back.user_id, c_back.data_to_read.message.id)
    else:
        rest_bot.edit_message_text(
            texts[c_back.get_rest_lang()]["EDIT_DISH_CHOSEN_MSG"](c_back.get_dish_name()),
            c_back.user_id,
            c_back.data_to_read.message.id
        )
        rest_bot.send_message(
            c_back.user_id,
            texts[c_back.get_rest_lang()]["EDIT_DISH_PARAM_MSG"],
            reply_markup=restaurant_menus.edit_dish_param_menu(c_back.get_rest_lang(), c_back)
        )


@rest_bot.callback_query_handler(
    func=lambda call: call.message.text in [lang["EDIT_DISH_PARAM_MSG"] for lang in texts.values()]
)
@logger_decorator_callback
def req_new_dish_param(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    rest_bot.delete_message(c_back.user_id, (c_back.data_to_read.message.id - 1))
    rest_bot.delete_message(c_back.user_id, c_back.data_to_read.message.id)
    request = c_back.data_to_read.data.split(maxsplit=1)
    if c_back.data_to_read.data == restaurant_menus.back_button(
            c_back.get_rest_lang()
    ).callback_data:
        rest_bot.delete_message(c_back.user_id, c_back.data_to_read.message.id)
    elif request[0] == "cat":
        rest_bot.send_message(
            c_back.user_id,
            texts[c_back.get_rest_lang()]["EDIT_CATEGORY_MSG"](request[1]),
            reply_markup=types.ForceReply()
        )
    elif request[0] == "des":
        rest_bot.send_message(
            c_back.user_id,
            texts[c_back.get_rest_lang()]["EDIT_DESCRIPTION_MSG"](request[1]),
            reply_markup=types.ForceReply()
        )
    elif request[0] == "prc":
        rest_bot.send_message(
            c_back.user_id,
            texts[c_back.get_rest_lang()]["EDIT_PRICE_MSG"](request[1]),
            reply_markup=types.ForceReply()
        )


@rest_bot.message_handler(
    func=lambda message: message.reply_to_message \
                         and message.reply_to_message.text \
                         in [
                             lang["EDIT_CATEGORY_MSG"](message.reply_to_message.text.split()[-1]) \
                                 for lang in texts.values()
                         ]
)
@logger_decorator_msg
def set_new_category(message: types.Message) -> None:
    """
    
    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    msg.edit_dish("category", message.reply_to_message.text.split()[-1])
    rest_bot.send_message(msg.user_id, texts[msg.get_rest_lang()]["CAT_SET_MSG"])


@rest_bot.message_handler(
    func=lambda message: message.reply_to_message \
                         and message.reply_to_message.text \
                         in [
                             lang["EDIT_DESCRIPTION_MSG"](
                                 message.reply_to_message.text.split()[-1]
                             ) for lang in texts.values()
                         ]
)
@logger_decorator_msg
def set_new_description(message: types.Message) -> None:
    """

    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    msg.edit_dish("dish_description", message.reply_to_message.text.split()[-1])
    rest_bot.send_message(msg.user_id, texts[msg.get_rest_lang()]["DESC_SET_MSG"])


@rest_bot.message_handler(
    func=lambda message: message.reply_to_message \
                         and message.reply_to_message.text \
                         in [
                             lang["EDIT_PRICE_MSG"](message.reply_to_message.text.split()[-1]) \
                                 for lang in texts.values()
                         ]
)
@logger_decorator_msg
def set_new_price(message: types.Message) -> None:
    """

    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    msg.data_to_read.text = float(msg.data_to_read.text.replace(",", "."))
    msg.edit_dish("dish_price", message.reply_to_message.text.split()[-1])
    rest_bot.send_message(msg.user_id, texts[msg.get_rest_lang()]["PRICE_SET_MSG"])


@rest_bot.message_handler(commands=["delete_dish"])
@logger_decorator_msg
def delete_dish_command(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    rest_bot.send_message(
        msg.user_id,
        texts[msg.get_rest_lang()]["DELETE_DISH_SELECT_MSG"],
        reply_markup=restaurant_menus.edit_dish_menu(msg.get_rest_lang(), msg)
    )


@rest_bot.callback_query_handler(
    func=lambda call: call.message.text \
                      in [lang["DELETE_DISH_SELECT_MSG"] for lang in texts.values()]
)
@logger_decorator_callback
def dish_deletion_select(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    rest_bot.delete_message(c_back.user_id, c_back.data_to_read.message.id)
    c_back.delete_dish()
    rest_bot.send_message(c_back.user_id, texts[c_back.get_rest_lang()]["DISH_DELETED_MSG"])


@rest_bot.message_handler(commands=["close_shift"])
@logger_decorator_msg
def close_shift_command(message: types.Message) -> None:
    """

    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    msg.close_shift()
    rest_bot.send_message(msg.user_id, texts[msg.get_rest_lang()]["CLOSE_SHIFT_MSG"])


@rest_bot.message_handler(commands=["open_shift"])
@logger_decorator_msg
def open_shift_command(message: types.Message) -> None:
    """

    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    msg.open_shift()
    rest_bot.send_message(msg.user_id, texts[msg.get_rest_lang()]["OPEN_SHIFT_MSG"])


@rest_bot.callback_query_handler(func=lambda call: "accepted" in call.data)
@logger_decorator_callback
def order_accepted(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    customer = c_back.get_customer()
    customer_info = c_back.get_customer_info()
    c_back.order_accepted()
    rest_location = c_back.get_rest_location()
    delivery_location = c_back.get_delivery_location()
    rest_bot.edit_message_reply_markup(c_back.user_id, c_back.data_to_read.message.id)
    rest_bot.send_message(
        c_back.user_id,
        texts[c_back.get_rest_lang()]["REST_ORDER_ACCEPTED_MSG"](
            c_back.data_to_read.data.split(maxsplit=1)[-1]
        )
    )
    cus_bot.send_message(
        customer[0],
        texts[customer[1]]["CUST_ORDER_ACCEPTED_MSG"](
            c_back.data_to_read.data.split(maxsplit=1)[-1]
        )
    )
    for courier in c_back.get_available_couriers():
        courier_bot.send_message(
            courier[0],
            texts[courier[1]]["LOOKING_FOR_COURIER_MSG"](
                c_back.data_to_read.data.split(maxsplit=1)[-1],
                c_back.get_courier_fee(),
                customer_info[0],
                customer_info[1],
                customer_info[2],
                customer_info[3],
                c_back.get_rest_name(),
                c_back.get_order_items(),
                rest_location[0]
            )
        )
        courier_bot.send_location(courier[0], rest_location[1][0], rest_location[1][1])
        courier_bot.send_message(courier[0], texts[courier[1]]["COURIER_DELIVERY_LOC_MSG"])
        courier_bot.send_location(courier[0], delivery_location[0][0], delivery_location[0][1])
        courier_bot.send_message(
            courier[0],
            texts[courier[1]]["COURIER_ACCEPT_ORDER_MSG"],
            reply_markup=restaurant_menus.courier_accept_menu(
                c_back.data_to_read.data.split(maxsplit=1)[-1],
                courier[1]
            )
        )


@rest_bot.callback_query_handler(func=lambda call: "ready" in call.data)
@logger_decorator_callback
def order_ready(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    courier = c_back.get_courier()
    customer = c_back.get_customer()
    c_back.order_ready()
    rest_bot.edit_message_text(
        texts[c_back.get_rest_lang()]["ORDER_READY_MSG"](
            c_back.data_to_read.data.split(maxsplit=1)[-1]
        ),
        c_back.user_id,
        c_back.data_to_read.message.id
    )
    courier_bot.send_message(
        courier[0],
        texts[courier[1]]["COUR_ORDER_IN_DELIVERY_MSG"](
            c_back.data_to_read.data.split(maxsplit=1)[-1]
        ),
        reply_markup=restaurant_menus.courier_in_delivery_menu(
            c_back.data_to_read.data.split(maxsplit=1)[-1],
            courier[1]
        )
    )
    cus_bot.send_message(
        customer[0],
        texts[customer[1]]["CUST_ORDER_IN_DELIVERY_MSG"](
            c_back.data_to_read.data.split(maxsplit=1)[-1]
        )
    )


def main():
    logger.info("The bot is running.")
    rest_bot.infinity_polling()


if __name__ == "__main__":
    main()
