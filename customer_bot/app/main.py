import telebot.types as types
from environs import Env
from telebot.apihelper import ApiTelegramException

import customer_menus
import tools.pp_tools as paypal
from customer_translations import texts
from customer_db_tools import Interface as DBInterface
from tools.bots_initialization import adm_bot, cus_bot, rest_bot
from tools.logger_tool import logger, logger_decorator_callback, logger_decorator_msg

env = Env()
env.read_env()

COURIER_FEE_BASE = env.float("COURIER_FEE_BASE", default=2.25)
COURIER_FEE_RATE = env.float("COURIER_FEE_RATE", default=0.08)
COURIER_FEE_DISTANCE_RATE = env.float("COURIER_FEE_DISTANCE_RATE", default=0.25)
SERVICE_FEE_BASE = env.float("SERVICE_FEE_BASE", default=1.75)
SERVICE_FEE_RATE = env.float("SERVICE_FEE_RATE", default=0.05)
MAX_PHONE_LENGTH = 11


# Auxiliary functions.
@logger_decorator_msg
def show_main_menu(message: types.Message) -> None:
    """Show Customer main menu if Customer is in the DB, otherwise call
    start().

    Args:
        message: Main menu request from Customer.

    """
    msg = DBInterface(message)
    if msg.user_in_db():
        cus_bot.send_message(
            msg.data_to_read.from_user.id,
            texts[msg.get_customer_lang()]["MAIN_MENU_MSG"],
            reply_markup=customer_menus.main_menu(msg.get_customer_lang())
        )
    else:
        start(msg.data_to_read)


@logger_decorator_msg
def phone_from_msg(message: types.Message) -> str:
    """Check if manually entered phone number is valid and add it into
    the DB.Customers if so.

    Args:
        message: Manually entered phone number.

    Returns:
        Phone number if valid, None otherwise.

    """
    msg = DBInterface(message)
    phone_number = "".join([symbol for symbol in str(msg.data_to_read.text) if symbol.isdigit()])
    if len(phone_number) not in range(2, (MAX_PHONE_LENGTH + 1)):
        return ""
    phone_number = "+" + phone_number
    msg.update_phone_number(phone_number)
    return phone_number


@logger_decorator_callback
def callback_to_msg(call: types.CallbackQuery) -> types.Message:
    """Extract types.Message object from types.CallbackQuery object
    replacing sender ID from bot's to Customer's one.

    Args:
        call: CallbackQuery object.

    Returns:
        Message object with Customer's ID in it.

    """
    call.message.from_user.id = call.from_user.id
    return call.message


@logger_decorator_callback
def clear_cart(call: types.CallbackQuery) -> None:
    """Clear Customer's cart on receiving corresponding callback query.

    Args:
        call: Callback query with Customer's cart deletion request.

    """
    callback = DBInterface(call)
    cus_bot.answer_callback_query(
        callback.data_to_read.id,
        texts[callback.get_customer_lang()]["DELETING_CART_ALERT"],
        show_alert=True
    )
    cus_bot.delete_message(callback.data_to_read.from_user.id, callback.data_to_read.message.id)
    callback.delete_cart()
    show_main_menu(callback_to_msg(callback.data_to_read))


@logger_decorator_callback
def prices_calc(call: types.CallbackQuery) -> None:
    """Calculate subtotal courier and service fees and total based on
    dishes in Customer's cart.

    Args:
        call: Callback query containing Customer's Telegram ID.

    """
    callback = DBInterface(call)
    subtotal = 0
    for dish in callback.get_from_cart("dishes_uuids"):
        callback.data_to_read.data = dish
        subtotal += callback.get_dish()[2]
    callback.data_to_read.data = subtotal
    callback.add_to_cart("subtotal")
    if subtotal > 0:
        courier_fee = round(
            (
                COURIER_FEE_BASE
                + float(subtotal)*COURIER_FEE_RATE
                + callback.get_delivery_distance()*COURIER_FEE_DISTANCE_RATE
            ),
            2
        )
        service_fee = round((SERVICE_FEE_BASE + float(subtotal)*SERVICE_FEE_RATE), 2)
    else:
        courier_fee = round(0, 2)
        service_fee = round(0, 2)
    callback.data_to_read.data = courier_fee
    callback.add_to_cart("courier_fee")
    callback.data_to_read.data = service_fee
    callback.add_to_cart("service_fee")
    callback.data_to_read.data = round((float(subtotal) + courier_fee + service_fee), 2)
    callback.add_to_cart("total")


# Sing in/sign up block.
@cus_bot.message_handler(commands=["start"])
@logger_decorator_msg
def start(message: types.Message) -> None:
    """Commence interaction between Customer and the bot. Check if
    Customer in the DB and start corresponding interaction sequence.

    Args:
        message: /start command from Customer.

    """
    msg = DBInterface(message)
    msg.delete_cart()
    if customer_name := msg.user_in_db():
        cus_bot.send_message(
            msg.data_to_read.from_user.id,
            texts[msg.get_customer_lang()]["WELCOME_BACK_MSG"](customer_name)
        )
        show_main_menu(msg.data_to_read)
    else:
        cus_bot.send_message(
            msg.data_to_read.from_user.id,
            texts[msg.get_customer_lang()]["FIRST_WELCOME_MSG"]
        )
        cus_bot.send_message(
            msg.data_to_read.from_user.id,
            texts[msg.get_customer_lang()]["ASK_AGREEMENT_MSG"],
            reply_markup=customer_menus.agreement_menu(msg.get_customer_lang())
        )


@cus_bot.message_handler(
    func=lambda message: message.text in [lang["SHOW_AGREEMENT_BTN"] for lang in texts.values()]
)
@logger_decorator_msg
def show_agreement(message: types.Message) -> None:
    """Show Customer agreement.

    Args:
        message: Show Agreement input from Customer.

    """
    msg = DBInterface(message)
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["AGREEMENT_TEXT"]
    )


@cus_bot.message_handler(
    func=lambda message: message.text in [lang["ACCEPT_AGREEMENT_BTN"] for lang in texts.values()]
)
@logger_decorator_msg
def agreement_accepted(message: types.Message) -> None:
    """Commence Customer sign up sequence. Add new Customer to the DB.

    Args:
        message: Accept Agreement input from Customer.

    """
    msg = DBInterface(message)
    if not msg.user_in_db():
        msg.add_customer()
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["AGREEMENT_ACCEPTED_MSG"]
    )
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["REG_NAME_MSG"],
        reply_markup=types.ForceReply(
            input_field_placeholder=texts[msg.get_customer_lang()]["REG_NAME_PLACEHOLDER"]
        )
    )


@cus_bot.message_handler(
    func=lambda message: message.reply_to_message \
                         and message.reply_to_message.text \
                         in [lang["REG_NAME_MSG"] for lang in texts.values()]
)
@logger_decorator_msg
def reg_name(message: types.Message) -> None:
    """Add Customer's name to the DB. Ask Customer to choose phone
    number input method.

    Args:
        message: Customer's name.

    """
    msg = DBInterface(message)
    msg.update_name()
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["REG_NAME_RECEIVED_MSG"](msg.data_to_read.text)
    )
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["REG_PHONE_METHOD_MSG"],
        reply_markup=customer_menus.reg_phone_menu(msg.get_customer_lang())
    )


@cus_bot.message_handler(content_types=["contact"])
@cus_bot.message_handler(
    func=lambda message: message.text in [lang["REG_PHONE_METHOD_MSG"] for lang in texts.values()]
)
@logger_decorator_msg
def contact(message: types.Message) -> None:
    """Add Customer's phone number imported via Telegram contact info
    into the DB. Ask Customer to provide delivery location.

    Args:
        message: Customer's Telegram contact info.

    """
    msg = DBInterface(message)
    phone_number = msg.data_to_read.contact.phone_number
    if phone_number[0] != "+":
        phone_number = "+" + phone_number
    msg.update_phone_number(phone_number)
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["PHONE_RECEIVED_MSG"](phone_number)
    )
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["REG_LOCATION_MSG"],
        reply_markup=customer_menus.reg_location_menu(msg.get_customer_lang())
    )


@cus_bot.message_handler(
    func=lambda message: message.text in [lang["REG_PHONE_MAN_BTN"] for lang in texts.values()]
)
@logger_decorator_msg
def reg_phone_str(message: types.Message) -> None:
    """Ask Customer to input phone number manually.

    Args:
        message: Request form Customer to input phone number manually.

    """
    msg = DBInterface(message)
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["REG_PHONE_MSG"],
        reply_markup=types.ForceReply(
            input_field_placeholder=texts[msg.get_customer_lang()]["REG_PHONE_PLACEHOLDER"]
        )
    )


@cus_bot.message_handler(
    func=lambda message: message.reply_to_message \
                         and message.reply_to_message.text \
                         in [lang["REG_PHONE_MSG"] for lang in texts.values()]
)
@logger_decorator_msg
def reg_phone(message: types.Message) -> None:
    """Check if phone number was added to the DB if manual input was
    chosen. Ask Customer to provide delivery location if so. Ask
    Customer to input phone number again otherwise.

    Args:
        message: Customer's phone number entered manually.

    """
    msg = DBInterface(message)
    if phone_number := phone_from_msg(message):
        cus_bot.send_message(
            msg.data_to_read.from_user.id,
            texts[msg.get_customer_lang()]["PHONE_RECEIVED_MSG"](phone_number)
        )
        cus_bot.send_message(
            msg.data_to_read.from_user.id,
            texts[msg.get_customer_lang()]["REG_LOCATION_MSG"],
            reply_markup=customer_menus.reg_location_menu(msg.get_customer_lang())
        )
    else:
        cus_bot.send_message(
            msg.data_to_read.from_user.id,
            texts[msg.get_customer_lang()]["INVALID_PHONE_MSG"]
        )
        cus_bot.send_message(
            msg.data_to_read.from_user.id,
            texts[msg.get_customer_lang()]["REG_PHONE_MSG"],
            reply_markup=types.ForceReply(
                input_field_placeholder=texts[msg.get_customer_lang()]["REG_PHONE_PLACEHOLDER"]
            )
        )


@cus_bot.message_handler(content_types=["location"])
@cus_bot.message_handler(
    func=lambda message: message.text in [lang["REG_LOCATION_BTN"] for lang in texts.values()]
)
@logger_decorator_msg
def reg_location(message: types.Message) -> None:
    """Add location to the DB. Proceed to main menu.

    Args:
        message: Location from Customer.

    """
    msg = DBInterface(message)
    msg.update_customer_location()
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["REG_LOCATION_RECEIVED_MSG"]
    )
    cus_bot.send_location(
        msg.data_to_read.from_user.id,
        msg.data_to_read.location.latitude,
        msg.data_to_read.location.longitude
    )
    show_main_menu(msg.data_to_read)


# Main menu block.
@cus_bot.message_handler(
    func=lambda message: message.text in [lang["OPTIONS_BTN"] for lang in texts.values()]
)
@logger_decorator_msg
def options(message: types.Message) -> None:
    """Show options menu.

    Args:
        message: Options request from Customer.

    """
    msg = DBInterface(message)
    cus_bot.delete_message(msg.data_to_read.from_user.id, msg.data_to_read.id)
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["OPTIONS_MSG"],
        reply_markup=customer_menus.options_menu(msg.get_customer_lang())
    )


@cus_bot.message_handler(
    func=lambda message: message.text in [lang["MY_ORDERS_BTN"] for lang in texts.values()]
)
@logger_decorator_msg
def my_orders(message: types.Message) -> None:
    """Send Customer their order history.

    Args:
        message: Message from Customer with corresponding request.

    """
    msg = DBInterface(message)
    if orders := msg.show_my_orders():
        while orders:
            cus_bot.send_message(
                msg.data_to_read.from_user.id,
                texts[msg.get_customer_lang()]["MY_ORDERS_MSG"](
                    orders,
                    texts[msg.get_customer_lang()]["STATUS_CODES"][orders[0][6]]
                )
            )
            orders.pop(0)
        show_main_menu(msg.data_to_read)
    else:
        cus_bot.send_message(
            msg.data_to_read.from_user.id,
            texts[msg.get_customer_lang()]["NO_ORDERS_FOUND_MSG"]
        )
        show_main_menu(msg.data_to_read)


@cus_bot.message_handler(
    func=lambda message: message.text in [lang["NEW_ORDER_BTN"] for lang in texts.values()]
)
@logger_decorator_msg
def new_order(message: types.Message) -> None:
    """Commence order creation sequence. Check if User location is
    provided. If location is provided, ask confirmation.

    Args:
        message: Request form Customer to create new order.

    """
    msg = DBInterface(message)
    cus_bot.delete_message(msg.data_to_read.from_user.id, msg.data_to_read.id)
    if not msg.check_couriers():
        cus_bot.send_message(
            msg.data_to_read.from_user.id,
            texts[msg.get_customer_lang()]["NO_COURIERS_MSG"]
        )
        show_main_menu(msg.data_to_read)
        return None
    if location := msg.check_if_location():
        cus_bot.send_message(
            msg.data_to_read.from_user.id,
            texts[msg.get_customer_lang()]["CONFIRM_LOCATION_MSG"],
            reply_markup=types.ReplyKeyboardRemove()
        )
        cus_bot.send_location(
            msg.data_to_read.from_user.id,
            location["lat"],
            location["lon"],
            reply_markup=customer_menus.confirm_location_menu(msg.get_customer_lang())
        )
    else:
        cus_bot.send_message(
            msg.data_to_read.from_user.id,
            texts[msg.get_customer_lang()]["LOCATION_NOT_FOUND_MSG"]
        )
        show_main_menu(msg.data_to_read)


# Options menu block.
@cus_bot.message_handler(
    func=lambda message: message.text in [lang["MAIN_MENU_BTN"] for lang in texts.values()]
)
@logger_decorator_msg
def main_menu(message: types.Message) -> None:
    """Get back to main menu.

    Args:
        message: Main menu request from Customer.

    """
    cus_bot.delete_message(message.from_user.id, message.id)
    show_main_menu(message)


@cus_bot.message_handler(
    func=lambda message: message.text in [lang["CONTACT_SUPPORT_BTN"] for lang in texts.values()]
)
@logger_decorator_msg
def contact_support(message: types.Message) -> None:
    """Start support request sequence.

    Args:
        message: Message from Customer with corresponding request.

    """
    msg = DBInterface(message)
    cus_bot.delete_message(msg.data_to_read.from_user.id, msg.data_to_read.id)
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["CUS_SUPPORT_MSG"],
        reply_markup=types.ForceReply()
    )


@cus_bot.message_handler(
    func=lambda message: message.reply_to_message \
                         and message.reply_to_message.text \
                         in [lang["CUS_SUPPORT_MSG"] for lang in texts.values()]
)
@logger_decorator_msg
def message_to_support(message: types.Message) -> None:
    """Forward message from Customer to Support.

    Args:
        message: Message from Customer to Support.

    """
    msg = DBInterface(message)
    support = msg.get_support()
    adm_bot.send_message(
        support[0],
        texts[support[1]]["SUPPORT_FR_CUS_MSG"](
            msg.data_to_read.from_user.username,
            msg.data_to_read.from_user.id,
            message.text
        )
    )
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["SUPPORT_SENT_MSG"]
    )
    show_main_menu(msg.data_to_read)


@cus_bot.message_handler(
    func=lambda message: message.text \
                         in [lang["RESET_CONTACT_INFO_BTN"] for lang in texts.values()]
)
@logger_decorator_msg
def reset_contact_info(message: types.Message) -> None:
    """Ask Customer for contact info reset confirmation.

    Args:
        message: Request form Customer to reset contact info.

    """
    msg = DBInterface(message)
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["RESET_CONTACT_INFO_MSG"],
        reply_markup=customer_menus.reset_info_menu(msg.get_customer_lang())
    )


@cus_bot.message_handler(
    func=lambda message: message.text in [lang["DELETE_PROFILE_BTN"] for lang in texts.values()]
)
@logger_decorator_msg
def delete_profile(message: types.Message) -> None:
    """Ask Customer for profile deletion confirmation.

    Args:
        message: Deletion request from Customer.

    """
    msg = DBInterface(message)
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["DELETE_PROFILE_MSG"],
        reply_markup=customer_menus.confirm_delete_profile_menu(msg.get_customer_lang())
    )


# Language change menu.
@cus_bot.message_handler(
    func=lambda message: message.text in [lang["CHANGE_LANG_BTN"] for lang in texts.values()]
)
@logger_decorator_msg
def change_lang_menu(message: types.Message) -> None:
    """Open language select menu.

    Args:
        message: Message from Customer with corresponding request.

    """
    msg = DBInterface(message)
    cus_bot.delete_message(msg.data_to_read.from_user.id, msg.data_to_read.id)
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["LANG_SEL_MENU"],
        reply_markup=types.ReplyKeyboardRemove()
    )
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["CHANGE_LANG_MSG"],
        reply_markup=customer_menus.lang_sel_menu(msg.get_customer_lang())
    )


@cus_bot.callback_query_handler(
    func=lambda call: call.message.text in [lang["CHANGE_LANG_MSG"] for lang in texts.values()]
)
@logger_decorator_callback
def lang_set(call: types.CallbackQuery) -> None:
    """Change bot interface language.

    Args:
        call: Callback query from Customer with selected language info.

    """
    callback = DBInterface(call)
    callback.set_customer_lang()
    cus_bot.delete_message(
        callback.data_to_read.from_user.id,
        (callback.data_to_read.message.id - 1)
    )
    cus_bot.delete_message(callback.data_to_read.from_user.id, callback.data_to_read.message.id)
    show_main_menu(callback_to_msg(callback.data_to_read))


# Contact Info reset block.
@cus_bot.message_handler(
    func=lambda message: message.text in [lang["CONFIRM_RESET_BTN"] for lang in texts.values()]
)
@logger_decorator_msg
def confirm_reset(message: types.Message) -> None:
    """Commence contact info reset sequence.

    Args:
        message: Confirmation from Customer.

    """
    msg = DBInterface(message)
    msg.delete_customer()
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["CONTACT_INFO_DELETED_MSG"]
    )
    agreement_accepted(message)


# Profile deletion block.
@cus_bot.message_handler(
    func=lambda message: message.text \
                         in [lang["CONFIRM_DELETE_PROFILE_BTN"] for lang in texts.values()]
)
@logger_decorator_msg
def confirm_delete(message: types.Message) -> None:
    """Delete Customer's profile from DB.

    Args:
        message: Confirmation from Customer.

    """
    msg = DBInterface(message)
    msg.delete_customer()
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["PROFILE_DELETED_MSG"],
        reply_markup=types.ReplyKeyboardRemove()
    )


# Creating order sequence block.
@cus_bot.callback_query_handler(func=lambda call: call.message.location)
@logger_decorator_callback
def check_location_confirmation(call: types.CallbackQuery) -> None:
    """Process Customer's response to location confirmation request.
    Show Customer restaurant type selection menu if confirmed, send back
    to main menu if not.

    Args:
        call: Callback query from Customer with response to location
            confirmation request.

    """
    callback = DBInterface(call)
    cus_bot.delete_message(callback.data_to_read.from_user.id, callback.data_to_read.message.id)
    cus_bot.delete_message(
        callback.data_to_read.from_user.id,
        (callback.data_to_read.message.id - 1)
    )
    if callback.data_to_read.data == texts[callback.get_customer_lang()]["WRONG_LOCATION_BTN"]:
        cus_bot.send_message(
            callback.data_to_read.from_user.id,
            texts[callback.get_customer_lang()]["REG_LOCATION_MSG"],
            reply_markup=customer_menus.reg_location_menu(callback.get_customer_lang())
        )
    elif callback.data_to_read.data == texts[callback.get_customer_lang()]["CONFIRM_LOCATION_BTN"]:
        callback.new_cart()
        cus_bot.send_message(
            callback.data_to_read.from_user.id,
            texts[callback.get_customer_lang()]["CHOOSE_REST_TYPE_MSG"],
            reply_markup=customer_menus.choose_rest_type_menu(callback.get_customer_lang())
        )


@cus_bot.callback_query_handler(
    func=lambda call: call.message.text \
                      in [lang["CHOOSE_REST_TYPE_MSG"] for lang in texts.values()]
)
@logger_decorator_callback
def rest_type_chosen(call: types.CallbackQuery) -> None:
    """Process Customer's response to restaurant type selection. Show
    Customer restaurants of selected type and add restaurant type to the
    Customer's cart or go back to main menu if "go back" button is
    clicked.
    
    Args:
        call: Callback query from Customer with response to restaurant
            type selection.

    """
    callback = DBInterface(call)
    if callback.data_to_read.data == customer_menus.back_button(
            callback.get_customer_lang()
    ).callback_data:
        cus_bot.answer_callback_query(
            callback.data_to_read.id,
            texts[callback.get_customer_lang()]["EXITING_ORDER_MENU_MSG"]
        )
        cus_bot.delete_message(
            callback.data_to_read.from_user.id,
            callback.data_to_read.message.id
        )
        callback.delete_cart()
        show_main_menu(callback_to_msg(callback.data_to_read))
    else:
        callback.add_to_cart("restaurant_type")
        cus_bot.edit_message_text(
            texts[callback.get_customer_lang()]["REST_TYPE_SELECTED_MSG"](
                callback.data_to_read.data
            ),
            callback.data_to_read.from_user.id,
            callback.data_to_read.message.id
        )
        cus_bot.send_message(
            callback.data_to_read.from_user.id,
            texts[callback.get_customer_lang()]["CHOOSE_REST_MSG"],
            reply_markup=customer_menus.choose_rest_menu(callback.get_customer_lang(), callback)
        )


@cus_bot.callback_query_handler(
    func=lambda call: call.message.text in [lang["CHOOSE_REST_MSG"] for lang in texts.values()]
)
@logger_decorator_callback
def restaurant_chosen(call: types.CallbackQuery) -> None:
    """Process Customer's response to restaurant selection. Show
    Customer dish types available in selected restaurant and add
    restaurant UUID to the Customer's cart or go back to main menu if
    "go back" button is clicked.

    Args:
        call: Callback query from Customer with response to restaurant
            selection.

    """
    callback = DBInterface(call)
    try:
        cus_bot.delete_message(
            callback.data_to_read.from_user.id,
            (callback.data_to_read.message.id - 1)
        )
    except ApiTelegramException:
        pass
    if callback.data_to_read.data == customer_menus.back_button(
            callback.get_customer_lang()
    ).callback_data:
        cus_bot.answer_callback_query(
            callback.data_to_read.id,
            texts[callback.get_customer_lang()]["DELETING_CART_ALERT"],
            show_alert=True
        )
        cus_bot.delete_message(
            callback.data_to_read.from_user.id,
            callback.data_to_read.message.id
        )
        callback.delete_cart()
        show_main_menu(callback_to_msg(callback.data_to_read))
    else:
        callback.add_to_cart("restaurant_uuid")
        cus_bot.edit_message_text(
            texts[callback.get_customer_lang()]["REST_SELECTED_MSG"](callback.rest_name_by_uuid()),
            callback.data_to_read.from_user.id,
            callback.data_to_read.message.id
        )
        cus_bot.send_message(
            callback.data_to_read.from_user.id,
            texts[callback.get_customer_lang()]["CHOOSE_DISH_CATEGORY_MSG"],
            reply_markup=customer_menus.choose_dish_cat_menu(
                callback.get_customer_lang(),
                callback
            )
        )


@cus_bot.callback_query_handler(
    func=lambda call: call.message.text \
                      in [lang["CHOOSE_DISH_CATEGORY_MSG"] for lang in texts.values()]
)
@logger_decorator_callback
def dish_category_chosen(call: types.CallbackQuery) -> None:
    """Process Customer's response to dish category selection. Show
    Customer dishes of selected category available in selected
    restaurant or go back to restaurant selection menu if "go back"
    button is clicked. Show Customer their cart or clear it if
    corresponding buttons are clicked.

    Args:
        call: Callback query from Customer with response to dish
            category selection.

    """
    callback = DBInterface(call)
    try:
        cus_bot.delete_message(
            callback.data_to_read.from_user.id,
            (callback.data_to_read.message.id - 1)
        )
    except ApiTelegramException:
        pass
    if callback.data_to_read.data == customer_menus.back_button(
            callback.get_customer_lang()
    ).callback_data:
        callback.delete_from_cart("restaurant_uuid")
        callback.data_to_read.data = callback.get_from_cart("restaurant_type")
        rest_type_chosen(callback.data_to_read)
    elif callback.data_to_read.data == customer_menus.cancel_order_button(
            callback.get_customer_lang()
    ).callback_data:
        clear_cart(callback.data_to_read)
    elif callback.data_to_read.data == customer_menus.cart_button(
            callback.get_customer_lang()
    ).callback_data:
        is_dish_added(callback.data_to_read)
    else:
        cus_bot.edit_message_text(
            texts[callback.get_customer_lang()]["DISH_CAT_SELECTED_MSG"](
                callback.data_to_read.data
            ),
            callback.data_to_read.from_user.id,
            callback.data_to_read.message.id
        )
        cus_bot.send_message(
            callback.data_to_read.from_user.id,
            texts[callback.get_customer_lang()]["CHOOSE_DISH_MSG"],
            reply_markup=customer_menus.choose_dish_menu(callback.get_customer_lang(), callback)
        )


@cus_bot.callback_query_handler(
    func=lambda call: call.message.text in [lang["CHOOSE_DISH_MSG"] for lang in texts.values()]
)
@logger_decorator_callback
def dish_chosen(call: types.CallbackQuery) -> None:
    """Process Customer's response to dish selection. Show Customer dish
    selection confirmation menu displaying dish description and price or
    go back to restaurant selection menu if "go back" button is clicked.
    Show Customer their cart or clear it if corresponding buttons are
    clicked.

    Args:
        call: Callback query from Customer with response to dish
            selection.

    """
    callback = DBInterface(call)
    try:
        cus_bot.delete_message(
            callback.data_to_read.from_user.id,
            (callback.data_to_read.message.id - 1)
        )
    except ApiTelegramException:
        pass
    if callback.data_to_read.data == customer_menus.back_button(
            callback.get_customer_lang()
    ).callback_data:
        callback.data_to_read.data = callback.get_from_cart("restaurant_uuid")
        restaurant_chosen(callback.data_to_read)
    elif callback.data_to_read.data == customer_menus.cancel_order_button(
            callback.get_customer_lang()
    ).callback_data:
        clear_cart(callback.data_to_read)
    elif callback.data_to_read.data == customer_menus.cart_button(
            callback.get_customer_lang()
    ).callback_data:
        is_dish_added(callback.data_to_read)
    else:
        cus_bot.edit_message_text(
            texts[callback.get_customer_lang()]["DISH_SELECTED_MSG"](callback.get_dish()),
            callback.data_to_read.from_user.id,
            callback.data_to_read.message.id
        )
        cus_bot.send_message(
            callback.data_to_read.from_user.id,
            texts[callback.get_customer_lang()]["ADD_DISH_MSG"],
            reply_markup=customer_menus.conf_sel_dish_menu(callback.get_customer_lang(), callback)
        )


@cus_bot.callback_query_handler(
    func=lambda call: call.message.text in [lang["ADD_DISH_MSG"] for lang in texts.values()]
)
@logger_decorator_callback
def is_dish_added(call: types.CallbackQuery) -> None:
    """Process Customer's response to selected dish confirmation. Show
    Customer's cart menu displaying dishes and price or go back to dish
    category selection menu if confirmation isn't obtained.

    Args:
        call: Callback query from Customer with response to selected
            dish confirmation.

    """
    callback = DBInterface(call)
    try:
        cus_bot.delete_message(
            callback.data_to_read.from_user.id,
            (callback.data_to_read.message.id - 1)
        )
    except ApiTelegramException:
        pass
    if callback.data_to_read.data == customer_menus.back_button(
            callback.get_customer_lang()
    ).callback_data:
        callback.data_to_read.data = callback.get_from_cart("restaurant_uuid")
        restaurant_chosen(callback.data_to_read)
    else:
        if callback.data_to_read.data != customer_menus.cart_button(
                callback.get_customer_lang()
        ).callback_data:
            new_callback = DBInterface(call)
            dishes_uuids = callback.get_from_cart("dishes_uuids")
            if not dishes_uuids:
                dishes_uuids = []
            dishes_uuids.append(callback.data_to_read.data)
            new_callback.data_to_read.data = dishes_uuids
            new_callback.add_to_cart("dishes_uuids")
            prices_calc(new_callback.data_to_read)
        callback.data_to_read.data = callback.get_from_cart("dishes_uuids")
        dishes = []
        if callback.data_to_read.data:
            for dish in callback.data_to_read.data:
                callback.data_to_read.data = dish
                dishes.append(callback.get_dish()[0])
        cus_bot.edit_message_text(
            texts[callback.get_customer_lang()]["YOUR_CART_MSG"](
                "\n".join(sorted(dishes)),
                callback.get_from_cart("subtotal"),
                callback.get_from_cart("courier_fee"),
                callback.get_from_cart("service_fee"),
                callback.get_from_cart("total")
            ),
            callback.data_to_read.from_user.id,
            callback.data_to_read.message.id
        )
        cus_bot.send_message(
            callback.data_to_read.from_user.id,
            texts[callback.get_customer_lang()]["CART_ACTIONS_MSG"],
            reply_markup=customer_menus.cart_menu(callback.get_customer_lang())
        )


@cus_bot.callback_query_handler(
    func=lambda call: call.message.text in [lang["CART_ACTIONS_MSG"] for lang in texts.values()]
)
@logger_decorator_callback
def cart_actions(call: types.CallbackQuery) -> None:
    """Process Customer's input from cart actions menu. Clear cart if
    corresponding button is clicked. Call item deletion menu on request.
    Return Customer to dish category selection menu on request. Generate
    payment URL and proceed to payment menu on request if payment URL
    has been generated successfully otherwise send "payment URL
    generation failed" message to Customer.

    Args:
        call: Callback query with Customer's input from cart actions
            menu.

    """
    callback = DBInterface(call)
    cus_bot.delete_message(
        callback.data_to_read.from_user.id,
        (callback.data_to_read.message.id - 1)
    )
    if callback.data_to_read.data == customer_menus.cancel_order_button(
            callback.get_customer_lang()
    ).callback_data:
        clear_cart(callback.data_to_read)
    elif callback.data_to_read.data == texts[callback.get_customer_lang()]["DELETE_ITEM_BTN"]:
        cus_bot.edit_message_text(
            texts[callback.get_customer_lang()]["DELETE_ITEM_MSG"],
            callback.data_to_read.from_user.id,
            callback.data_to_read.message.id,
            reply_markup=customer_menus.item_deletion_menu(callback.get_customer_lang(), callback)
        )
    elif callback.data_to_read.data == texts[callback.get_customer_lang()]["ADD_MORE_BTN"]:
        callback.data_to_read.data = callback.get_from_cart("restaurant_uuid")
        callback.data_to_read.message.text = texts[callback.get_customer_lang()]["ADD_MORE_BTN"]
        restaurant_chosen(callback.data_to_read)
    elif callback.data_to_read.data == texts[callback.get_customer_lang()]["ADD_COMMENT_BTN"]:
        cus_bot.delete_message(
            callback.data_to_read.from_user.id,
            callback.data_to_read.message.id
        )
        cus_bot.send_message(
            callback.data_to_read.from_user.id,
            texts[callback.get_customer_lang()]["ADD_COMMENT_MSG"],
            reply_markup=types.ForceReply()
        )
    elif callback.data_to_read.data == texts[callback.get_customer_lang()]["MAKE_ORDER_BTN"]:
        order_info = callback.order_creation()
        if paypal_order_info := paypal.pp_order_creation(order_info[0]):
            payment_url = paypal_order_info["URL"]
            pp_order_id = paypal_order_info["order_id"]
            callback.update_order(order_info[0], "paypal_order_id", pp_order_id)
            cus_bot.edit_message_text(
                texts[callback.get_customer_lang()]["ORDER_CREATED_MSG"](order_info),
                callback.data_to_read.from_user.id,
                callback.data_to_read.message.id
            )
            cus_bot.send_message(
                callback.data_to_read.from_user.id,
                texts[callback.get_customer_lang()]["PAYMENT_MENU_MSG"](payment_url),
                reply_markup=customer_menus.payment_menu(
                    callback.get_customer_lang(),
                    order_info[0]
                )
            )
        else:
            cus_bot.send_message(
                callback.data_to_read.from_user.id,
                texts[callback.get_customer_lang()]["PAYPAL_ORDER_CREATION_FAIL_MSG"]
            )


@cus_bot.message_handler(
    func=lambda message: message.reply_to_message \
                         and message.reply_to_message.text \
                         in [lang["ADD_COMMENT_MSG"] for lang in texts.values()]
)
@logger_decorator_msg
def add_comment_menu(message: types.Message) -> None:
    """Add comment for order.

    Args:
        message: Message with comment.

    """
    msg = DBInterface(message)
    msg.data_to_read.data = msg.data_to_read.text
    msg.add_to_cart("order_comment")
    cus_bot.delete_message(msg.data_to_read.from_user.id, msg.data_to_read.id)
    cus_bot.delete_message(msg.data_to_read.from_user.id, msg.data_to_read.reply_to_message.id)
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["COMMENT_ADDED_MSG"]
    )
    cus_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_customer_lang()]["TO_CART_MSG"],
        reply_markup=customer_menus.comment_menu(msg.get_customer_lang())
    )


@cus_bot.callback_query_handler(
    func=lambda call: call.data in [lang["CART_BTN"] for lang in texts.values()]
)
@logger_decorator_callback
def return_to_cart_after_comment(call: types.CallbackQuery) -> None:
    """Return Customer to cart menu after comment addition.

    Args:
        call: Callback query from Customer.

    """
    dish_chosen(call)


@cus_bot.callback_query_handler(
    func=lambda call: call.message.text in [lang["DELETE_ITEM_MSG"] for lang in texts.values()]
)
@logger_decorator_callback
def item_deletion(call: types.CallbackQuery) -> None:
    """Delete selected item from Customer's cart. Call cart menu.

    Args:
        call: Callback query with Customer's input from item deletion
            menu.

    """
    callback = DBInterface(call)
    if callback.data_to_read.data != customer_menus.cart_button(
            callback.get_customer_lang()
    ).callback_data:
        if dishes_uuids := callback.get_from_cart("dishes_uuids"):
            dishes_uuids.remove(callback.data_to_read.data)
            callback.data_to_read.data = dishes_uuids
            callback.add_to_cart("dishes_uuids")
        prices_calc(callback.data_to_read)
    callback.data_to_read.data = customer_menus.cart_button(
        callback.get_customer_lang()
    ).callback_data
    is_dish_added(callback.data_to_read)


# Payment block.
@cus_bot.callback_query_handler(func=lambda call: "paid" in call.data)
@logger_decorator_callback
def order_paid(call: types.CallbackQuery) -> None:
    """Process "paid" button, Send payment capture request to PayPal and
    send order to the Restaurant if payment was captured.

    Args:
        call: Callback query from "paid" button with order UUID in it.

    """
    callback = DBInterface(call)
    if paypal.pp_capture_order(callback.data_to_read.data.split(maxsplit=1)[1]):
        callback.update_order(callback.data_to_read.data.split(maxsplit=1)[1], "order_status", "2")
        rest_bot.send_message(
            callback.get_order_info(
                callback.data_to_read.data.split(maxsplit=1)[1],
                "restaurant_id"
            ),
            texts[
                callback.get_restaurant_lang(
                    callback.get_order_info(
                        callback.data_to_read.data.split(maxsplit=1)[1],
                        "restaurant_uuid"
                    )
                )
            ]["REST_NEW_ORDER_MSG"](
                callback.data_to_read.data.split(maxsplit=1)[1],
                callback.get_order_info(callback.data_to_read.data.split(maxsplit=1)[1], "dishes"),
                callback.get_order_info(
                    callback.data_to_read.data.split(maxsplit=1)[1],
                    "dishes_subtotal"
                ),
                callback.get_order_info(
                    callback.data_to_read.data.split(maxsplit=1)[1],
                    "order_comment"
                )
            ),
            reply_markup=customer_menus.rest_accept_order_menu(
                callback.get_restaurant_lang(
                    callback.get_order_info(
                        callback.data_to_read.data.split(maxsplit=1)[1],
                        "restaurant_uuid"
                    )
                ),
                callback.data_to_read.data.split(maxsplit=1)[1]
            )
        )
        cus_bot.edit_message_text(
            texts[callback.get_customer_lang()]["CUS_PAYMENT_CONFIRMED_MSG"](
                callback.data_to_read.data.split(maxsplit=1)[1]
            ),
            callback.data_to_read.from_user.id,
            callback.data_to_read.message.id
        )
        paypal.pp_rest_payout(callback.data_to_read.data.split(maxsplit=1)[1])
        callback.delete_cart()
        show_main_menu(callback_to_msg(callback.data_to_read))
    else:
        cus_bot.send_message(
            callback.data_to_read.from_user.id,
            texts[callback.get_customer_lang()]["WAIT_FOR_CONFIRMATION_MSG"](
                callback.data_to_read.data.split(maxsplit=1)[1]
            )
        )


@cus_bot.callback_query_handler(func=lambda call: "order_closed" in call.data)
@logger_decorator_callback
def order_closed(call: types.CallbackQuery) -> None:
    """Process confirmation of order receiving from Customer.

    Args:
        call: Callback query from "Order received" button with order
            UUID in it.

    """
    callback = DBInterface(call)
    callback.close_order()
    cus_bot.edit_message_reply_markup(
        callback.data_to_read.from_user.id,
        callback.data_to_read.message.id
    )
    cus_bot.send_message(
        callback.data_to_read.from_user.id,
        texts[callback.get_customer_lang()]["ORDER_CLOSED_MSG"](
            callback.data_to_read.data.split(maxsplit=1)[-1]
        )
    )


@cus_bot.callback_query_handler(func=lambda call: "cancel" in call.data)
@logger_decorator_callback
def cancel(call: types.CallbackQuery) -> None:
    """Process order cancellation button after order is already created.

    Args:
        call: Callback query from "Cancel order" button with order UUID
            in it.

    """
    callback = DBInterface(call)
    callback.delete_cart()
    callback.update_order(callback.data_to_read.data.split(maxsplit=1)[-1], "order_status", "-1")
    cus_bot.edit_message_text(
        texts[callback.get_customer_lang()]["CANCEL_MSG"](
            callback.data_to_read.data.split(maxsplit=1)[-1]
        ),
        callback.data_to_read.from_user.id,
        callback.data_to_read.message.id
    )
    show_main_menu(callback_to_msg(callback.data_to_read))


def main():
    logger.info("The bot is running.")
    cus_bot.infinity_polling()


if __name__ == "__main__":
    main()
