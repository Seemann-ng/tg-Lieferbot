import telebot.types as types

import restaurant_menus
from restaurant_translations import texts
from restaurant_db_tools import Interface as DBInterface
from tools.bots_initialization import adm_bot, courier_bot, cus_bot, rest_bot
from tools.logger_tool import logger, logger_decorator_msg, logger_decorator_callback


@rest_bot.message_handler(commands=["start"])
@logger_decorator_msg
def start(message: types.Message) -> None:
    """Process /start command from the User.

    Args:
        message: /start command.

    """
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
    """Send registration request to an Admin.

    Args:
        message: Registration request.

    """
    msg = DBInterface(message)
    support = msg.get_support()
    adm_bot.send_message(
        support[0],
        texts[support[1]]["REG_REQUEST_MSG"](
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
    callback = DBInterface(call)
    callback.set_restaurant_lang()
    rest_bot.delete_message(
        callback.data_to_read.from_user.id,
        (callback.data_to_read.message.id - 1)
    )
    rest_bot.delete_message(callback.data_to_read.from_user.id, callback.data_to_read.message.id)
    rest_bot.send_message(
        callback.data_to_read.from_user.id,
        texts[callback.data_to_read.data]["LANG_SELECTED_MSG"]
    )


@rest_bot.message_handler(commands=["item_available"])
@logger_decorator_msg
def dish_available_command(message: types.Message) -> None:
    """Process /item_available command from User.

    Args:
        message: /item_available command.

    """
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
    """Process User input from "dish available" menu.

    Args:
        call: Callback query with selected dish info.

    """
    callback = DBInterface(call)
    callback.set_dish_available()
    rest_bot.delete_message(callback.user_id, callback.data_to_read.message.id)
    rest_bot.send_message(
        callback.user_id,
        texts[callback.get_rest_lang()]["DISH_SET_AVAILABLE_MSG"]
    )


@rest_bot.message_handler(commands=["item_unavailable"])
@logger_decorator_msg
def dish_unavailable_command(message: types.Message) -> None:
    """Process /item_unavailable command from User.

    Args:
        message: /item_unavailable command.

    """
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
    """Process User input from "dish unavailable" menu.

    Args:
        call: Callback query with selected dish info.

    """
    callback = DBInterface(call)
    rest_bot.delete_message(callback.user_id, callback.data_to_read.message.id)
    callback.set_dish_unavailable()
    rest_bot.send_message(
        callback.user_id,
        texts[callback.get_rest_lang()]["DISH_SET_UNAVAILABLE_MSG"]
    )


@rest_bot.message_handler(commands=["add_item"])
@logger_decorator_msg
def add_dish_command(message: types.Message) -> None:
    """Process /add_item command from User.

    Args:
        message: /add_item command with dish name.

    """
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


@rest_bot.message_handler(commands=["edit_item"])
@logger_decorator_msg
def edit_dish_command(message: types.Message) -> None:
    """Process /edit_item command from User.
    
    Args:
        message: /edit_item command.

    """
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
    """Process User input from "edit_dish" menu.
    
    Args:
        call: Callback query with selected dish.

    """
    callback = DBInterface(call)
    if callback.data_to_read.data == restaurant_menus.back_button(
            callback.get_rest_lang()
    ).callback_data:
        rest_bot.delete_message(callback.user_id, callback.data_to_read.message.id)
    else:
        rest_bot.edit_message_text(
            texts[callback.get_rest_lang()]["EDIT_DISH_CHOSEN_MSG"](callback.get_dish_name()),
            callback.user_id,
            callback.data_to_read.message.id
        )
        rest_bot.send_message(
            callback.user_id,
            texts[callback.get_rest_lang()]["EDIT_DISH_PARAM_MSG"],
            reply_markup=restaurant_menus.edit_dish_param_menu(callback.get_rest_lang(), callback)
        )


@rest_bot.callback_query_handler(
    func=lambda call: call.message.text in [lang["EDIT_DISH_PARAM_MSG"] for lang in texts.values()]
)
@logger_decorator_callback
def req_new_dish_param(call: types.CallbackQuery) -> None:
    """Process User input from "parameter_selection" menu.

    Args:
        call: Callback query with selected parameter and dish UUID.

    """
    callback = DBInterface(call)
    rest_bot.delete_message(callback.user_id, (callback.data_to_read.message.id - 1))
    rest_bot.delete_message(callback.user_id, callback.data_to_read.message.id)
    request = callback.data_to_read.data.split(maxsplit=1)
    if callback.data_to_read.data == restaurant_menus.back_button(
            callback.get_rest_lang()
    ).callback_data:
        rest_bot.delete_message(callback.user_id, callback.data_to_read.message.id)
    elif request[0] == "cat":
        rest_bot.send_message(
            callback.user_id,
            texts[callback.get_rest_lang()]["EDIT_CATEGORY_MSG"](request[1]),
            reply_markup=types.ForceReply()
        )
    elif request[0] == "des":
        rest_bot.send_message(
            callback.user_id,
            texts[callback.get_rest_lang()]["EDIT_DESCRIPTION_MSG"](request[1]),
            reply_markup=types.ForceReply()
        )
    elif request[0] == "prc":
        rest_bot.send_message(
            callback.user_id,
            texts[callback.get_rest_lang()]["EDIT_PRICE_MSG"](request[1]),
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
    """Set new category for selected dish.
    
    Args:
        message: New category for selected dish.

    """
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
    """Set new description for selected dish.

    Args:
        message: New dish description.

    """
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
    """Set new price for selected dish.

    Args:
        message: New price for selected dish.

    """
    msg = DBInterface(message)
    msg.data_to_read.text = float(msg.data_to_read.text.replace(",", "."))
    msg.edit_dish("dish_price", message.reply_to_message.text.split()[-1])
    rest_bot.send_message(msg.user_id, texts[msg.get_rest_lang()]["PRICE_SET_MSG"])


@rest_bot.message_handler(commands=["delete_item"])
@logger_decorator_msg
def delete_dish_command(message: types.Message) -> None:
    """Process /delete_item command.

    Args:
        message: /delete_item command.

    """
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
    """Process User input from "delete_dish" menu.

    Args:
        call: Callback query with selected dish UUID.

    """
    callback = DBInterface(call)
    rest_bot.delete_message(callback.user_id, callback.data_to_read.message.id)
    callback.delete_dish()
    rest_bot.send_message(callback.user_id, texts[callback.get_rest_lang()]["DISH_DELETED_MSG"])


@rest_bot.message_handler(commands=["close_shift"])
@logger_decorator_msg
def close_shift_command(message: types.Message) -> None:
    """Mark Restaurant in the database as currently not working.

    Args:
        message: /close_shift command.

    """
    msg = DBInterface(message)
    msg.close_shift()
    rest_bot.send_message(msg.user_id, texts[msg.get_rest_lang()]["CLOSE_SHIFT_MSG"])


@rest_bot.message_handler(commands=["open_shift"])
@logger_decorator_msg
def open_shift_command(message: types.Message) -> None:
    """Mark Restaurant in the database as currently working.

    Args:
        message: /open_shift command.

    """
    msg = DBInterface(message)
    msg.open_shift()
    rest_bot.send_message(msg.user_id, texts[msg.get_rest_lang()]["OPEN_SHIFT_MSG"])


@rest_bot.message_handler(commands=["support"])
@logger_decorator_msg
def contact_support(message: types.Message) -> None:
    """Start support request sequence.

    Args:
        message: Message from restaurant with corresponding request.

    """
    msg = DBInterface(message)
    rest_bot.delete_message(msg.data_to_read.from_user.id, msg.data_to_read.id)
    rest_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_rest_lang()]["REST_SUPPORT_MSG"],
        reply_markup=types.ForceReply()
    )


@courier_bot.message_handler(
    func=lambda message: message.reply_to_message \
                         and message.reply_to_message.text \
                         in [lang["REST_SUPPORT_MSG"] for lang in texts.values()]
)
@logger_decorator_msg
def message_to_support(message: types.Message) -> None:
    """Forward message from Restaurant to Support.

    Args:
        message: Message from Restaurant to Support.

    """
    msg = DBInterface(message)
    support = msg.get_support()
    adm_bot.send_message(
        support[0],
        texts[support[1]]["SUPPORT_FR_REST_MSG"](
            msg.data_to_read.from_user.username,
            msg.data_to_read.from_user.id,
            message.text
        )
    )
    rest_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_rest_lang()]["SUPPORT_SENT_MSG"]
    )


@rest_bot.callback_query_handler(func=lambda call: "accepted" in call.data)
@logger_decorator_callback
def order_accepted(call: types.CallbackQuery) -> None:
    """Accept incoming order and send request to available Couriers.

    Args:
        call: Callback query with order UUID.

    """
    callback = DBInterface(call)
    customer = callback.get_customer()
    customer_info = callback.get_customer_info()
    callback.order_accepted()
    rest_location = callback.get_rest_location()
    delivery_location = callback.get_delivery_location()
    rest_bot.edit_message_reply_markup(callback.user_id, callback.data_to_read.message.id)
    rest_bot.send_message(
        callback.user_id,
        texts[callback.get_rest_lang()]["REST_ORDER_ACCEPTED_MSG"](
            callback.data_to_read.data.split(maxsplit=1)[-1]
        )
    )
    cus_bot.send_message(
        customer[0],
        texts[customer[1]]["CUST_ORDER_ACCEPTED_MSG"](
            callback.data_to_read.data.split(maxsplit=1)[-1]
        )
    )
    for courier in callback.get_available_couriers():
        courier_bot.send_message(
            courier[0],
            texts[courier[1]]["LOOKING_FOR_COURIER_MSG"](
                callback.data_to_read.data.split(maxsplit=1)[-1],
                callback.get_courier_fee(),
                customer_info[0],
                customer_info[1],
                customer_info[2],
                customer_info[3],
                callback.get_rest_name(),
                callback.get_order_items(),
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
                callback.data_to_read.data.split(maxsplit=1)[-1],
                courier[1]
            )
        )


@rest_bot.callback_query_handler(func=lambda call: "ready" in call.data)
@logger_decorator_callback
def order_ready(call: types.CallbackQuery) -> None:
    """Mark order as ready and handled to a Courier.

    Args:
        call: Callback query with order UUID.

    Returns:

    """
    callback = DBInterface(call)
    courier = callback.get_courier()
    customer = callback.get_customer()
    callback.order_ready()
    rest_bot.edit_message_text(
        texts[callback.get_rest_lang()]["ORDER_READY_MSG"](
            callback.data_to_read.data.split(maxsplit=1)[-1]
        ),
        callback.user_id,
        callback.data_to_read.message.id
    )
    courier_bot.send_message(
        courier[0],
        texts[courier[1]]["COUR_ORDER_IN_DELIVERY_MSG"](
            callback.data_to_read.data.split(maxsplit=1)[-1]
        ),
        reply_markup=restaurant_menus.courier_in_delivery_menu(
            callback.data_to_read.data.split(maxsplit=1)[-1],
            courier[1]
        )
    )
    cus_bot.send_message(
        customer[0],
        texts[customer[1]]["CUST_ORDER_IN_DELIVERY_MSG"](
            callback.data_to_read.data.split(maxsplit=1)[-1]
        )
    )


def main():
    logger.info("The bot is running.")
    rest_bot.infinity_polling()


if __name__ == "__main__":
    main()
