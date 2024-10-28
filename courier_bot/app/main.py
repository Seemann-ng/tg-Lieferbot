import telebot.types as types

import courier_menus
from courier_translations import texts
from courier_db_tools import Interface as DBInterface
from tools.bots_initialization import adm_bot, courier_bot, cus_bot, rest_bot
from tools.logger_tool import logger, logger_decorator_callback, logger_decorator_msg


@courier_bot.message_handler(commands=["start"])
@logger_decorator_msg
def start(message: types.Message) -> None:
    """Start interaction with bot; ask to send registration request to
    Admin, if User is not in courier database.

    Args:
        message: /start command message.

    """
    msg = DBInterface(message)
    if not msg.courier_in_db():
        courier_bot.send_message(
            msg.courier_id,
            texts[msg.get_courier_lang()]["ASK_REG_MSG"],
            reply_markup=types.ForceReply()
        )
    else:
        courier_bot.send_message(msg.courier_id, texts[msg.get_courier_lang()]["WELCOME_MSG"])


@courier_bot.message_handler(
    func=lambda message: message.reply_to_message \
                         and message.reply_to_message.text \
                         in [lang["ASK_REG_MSG"] for lang in texts.values()]
)
@logger_decorator_msg
def ask_registration(message: types.Message) -> None:
    """Process Courier registration request to Admin.

    Args:
        message: Courier registration request message.

    """
    msg = DBInterface(message)
    adm_bot.send_message(
        msg.get_support_id(),
        texts[msg.get_courier_lang()]["REG_REQ_MSG"](
            msg.data_to_read.from_user.username,
            msg.courier_id,
            message.text
        )
    )
    courier_bot.send_message(msg.courier_id, texts[msg.get_courier_lang()]["REG_REQ_SENT_MSG"])


@courier_bot.message_handler(commands=["select_language"])
@logger_decorator_msg
def change_lang_menu(message: types.Message) -> None:
    """Open language select menu.

    Args:
        message: Command with language select request.

    """
    msg = DBInterface(message)
    courier_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_courier_lang()]["LANG_SEL_MENU"]
    )
    courier_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_courier_lang()]["CHANGE_LANG_MSG"],
        reply_markup=courier_menus.lang_sel_menu(msg.get_courier_lang())
    )


@courier_bot.callback_query_handler(
    func= lambda call: call.message.text \
                       in [lang["CHANGE_LANG_MSG"] for lang in texts.values()]
)
@logger_decorator_callback
def lang_set(call: types.CallbackQuery) -> None:
    """Change bot interface language.

    Args:
        call: Callback query with selected language info.

    """
    callback = DBInterface(call)
    callback.set_courier_lang()
    courier_bot.delete_message(
        callback.data_to_read.from_user.id,
        (callback.data_to_read.message.id - 1)
    )
    courier_bot.delete_message(
        callback.data_to_read.from_user.id,
        callback.data_to_read.message.id
    )
    courier_bot.send_message(
        callback.data_to_read.from_user.id,
        texts[callback.data_to_read.data]["LANG_SELECTED_MSG"]
    )


@courier_bot.message_handler(commands=["balance"])
@logger_decorator_msg
def balance_command(message: types.Message) -> None:
    """Display Courier's salary balance.

    Args:
        message: /balance command message.

    """
    msg = DBInterface(message)
    courier_bot.send_message(
        msg.courier_id,
        texts[msg.get_courier_lang()]["BALANCE_MSG"](msg.get_salary_balance())
    )


@courier_bot.message_handler(commands=["change_transport"])
@logger_decorator_msg
def select_transport_command(message: types.Message) -> None:
    """Display transport choice menu.

    Args:
        message: /change_transport command message.

    """
    msg = DBInterface(message)
    courier_bot.send_message(
        msg.courier_id,
        texts[msg.get_courier_lang()]["CHANGE_TRANSPORT_MENU"],
        reply_markup=courier_menus.transport_menu(msg.get_courier_lang())
    )


@courier_bot.callback_query_handler(func=lambda call: "type" in call.data)
@logger_decorator_callback
def change_transport(call: types.CallbackQuery) -> None:
    """Process Courier transport choice menu input.

    Args:
        call: Callback query with selected transport type info.

    """
    callback = DBInterface(call)
    callback.set_courier_type()
    courier_bot.edit_message_text(
        texts[callback.get_courier_lang()]["TRANSPORT_SELECTED_MSG"],
        callback.courier_id,
        callback.data_to_read.message.id
    )


@courier_bot.message_handler(commands=["open_shift"])
@logger_decorator_msg
def open_shift_command(message: types.Message) -> None:
    """Process request to open shift.

    Args:
        message: /open_shift command message.

    """
    msg = DBInterface(message)
    msg.open_shift()
    courier_bot.send_message(msg.courier_id, texts[msg.get_courier_lang()]["OPEN_SHIFT_MSG"])


@courier_bot.message_handler(commands=["close_shift"])
@logger_decorator_msg
def close_shift_command(message: types.Message) -> None:
    """Process request to close shift.

    Args:
        message: /close_shift command message.

    """
    msg = DBInterface(message)
    if msg.check_occupied():
        courier_bot.send_message(
            msg.courier_id,
            texts[msg.get_courier_lang()]["CANNOT_CLOSE_SHIFT_MSG"]
        )
    else:
        msg.close_shift()
        courier_bot.send_message(msg.courier_id, texts[msg.get_courier_lang()]["CLOSE_SHIFT_MSG"])


@courier_bot.callback_query_handler(func=lambda call: "accept" in call.data)
@logger_decorator_callback
def accept_order(call: types.CallbackQuery) -> None:
    """Process request to accept order.

    Args:
        call: Callback query with request to accept order.

    """
    callback = DBInterface(call)
    courier_bot.edit_message_reply_markup(
        callback.data_to_read.from_user.id,
        callback.data_to_read.message.id
    )
    if callback.cur_accept_order():
        courier_bot.edit_message_text(
            texts[callback.get_courier_lang()]["COUR_ORDER_ACCEPTED_MSG"](
                callback.data_to_read.data.split(maxsplit=1)[-1]
            ),
            callback.data_to_read.from_user.id,
            callback.data_to_read.message.id
        )
        customer_info = callback.get_customer_info()
        courier_info = callback.get_courier_info()
        cus_bot.send_message(
            customer_info[0],
            texts[customer_info[1]]["COURIER_FOUND_MSG"](
                callback.data_to_read.data.split(maxsplit=1)[-1],
                courier_info[0],
                courier_info[1],
                courier_info[2]
            )
        )
        rest_info = callback.get_rest_info()
        rest_bot.send_message(
            rest_info[0],
            texts[rest_info[1]]["COURIER_FOUND_MSG"](
                callback.data_to_read.data.split(maxsplit=1)[-1],
                courier_info[0],
                courier_info[1],
                courier_info[2]
            )
        )
        rest_bot.send_message(
            rest_info[0],
            texts[rest_info[1]]["REST_ORDER_READY_MSG"](
                callback.data_to_read.data.split(maxsplit=1)[-1]
            ),
            reply_markup=courier_menus.rest_order_ready_menu(
                rest_info[1],
                callback.data_to_read.data.split(maxsplit=1)[-1]
            )
        )
    else:
        courier_bot.edit_message_text(
            texts[callback.get_courier_lang()]["ORDER_ALREADY_ACCEPTED_MSG"],
            callback.data_to_read.from_user.id,
            callback.data_to_read.message.id
        )


@courier_bot.callback_query_handler(func=lambda call: "in_delivery" in call.data)
@logger_decorator_callback
def in_delivery(call: types.CallbackQuery) -> None:
    """Process confirmation from Courier that order has been received
    in delivery.

    Args:
        call: Callback query with confirmation and order UUID.

    """
    callback = DBInterface(call)
    customer_info = callback.get_customer_info()
    callback.order_in_delivery()
    courier_bot.edit_message_reply_markup(callback.courier_id, callback.data_to_read.message.id)
    courier_bot.send_message(
        callback.courier_id,
        texts[callback.get_courier_lang()]["COUR_IN_DELIVERY_MSG"](
            callback.data_to_read.data.split(maxsplit=1)[-1]
        ),
        reply_markup=courier_menus.order_in_delivery_menu(
            callback.get_courier_lang(),
            callback.data_to_read.data.split(maxsplit=1)[-1]
        )
    )
    cus_bot.send_message(
        customer_info[0],
        texts[customer_info[1]]["CUS_IN_DELIVERY_MSG"](
            callback.data_to_read.data.split(maxsplit=1)[-1]
        )
    )


@courier_bot.callback_query_handler(func=lambda call: "delivered" in call.data)
@logger_decorator_callback
def delivered(call: types.CallbackQuery) -> None:
    """Process confirmation from Courier that order has been delivered.

    Args:
        call: Callback query with confirmation and order UUID.

    """
    callback = DBInterface(call)
    customer_info = callback.get_customer_info()
    callback.order_delivered()
    courier_bot.edit_message_reply_markup(callback.courier_id, callback.data_to_read.message.id)
    courier_bot.send_message(
        callback.courier_id,
        texts[callback.get_courier_lang()]["COUR_DELIVERED_MSG"](
            callback.data_to_read.data.split(maxsplit=1)[-1]
        )
    )
    cus_bot.send_message(
        customer_info[0],
        texts[customer_info[1]]["CUS_DELIVERED_MSG"](
            callback.data_to_read.data.split(maxsplit=1)[-1]
        ),
        reply_markup=courier_menus.cus_delivered_menu(
            customer_info[1],
            callback.data_to_read.data.split(maxsplit=1)[-1]
        )
    )


def main():
    logger.info("Bot is running")
    courier_bot.infinity_polling()


if __name__ == '__main__':
    main()
