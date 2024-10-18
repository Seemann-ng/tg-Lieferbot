import telebot.types as types
from telebot.apihelper import ApiTelegramException

import customer_menus
from customer_translations import texts
from customer_db_tools import Interface as DBInterface
from tools.bots_initialization import adm_bot, cus_bot
from tools.logger_tool import logger, logger_decorator_callback, logger_decorator_msg


# Auxiliary functions.
@logger_decorator_msg
def show_main_menu(message: types.Message) -> None:
    """Show Customer main menu if Customer is in the DB, otherwise call start().

    Args:
        message: Main menu request from Customer.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    if msg.user_in_db():
        customer_id = msg.data_to_read.from_user.id
        cus_bot.send_message(customer_id,
                             texts[lang_code]["MAIN_MENU_MSG"],
                             reply_markup=customer_menus.main_menu(lang_code))
    else:
        start(msg.data_to_read)


@logger_decorator_msg
def phone_from_msg(message: types.Message) -> str | None:
    """Check if manually entered phone number is valid and add it into the DB.Customers if so.

    Args:
        message: Manually entered phone number.

    Returns:
        Phone number if valid, None otherwise.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    phone_number = "".join([symbol for symbol in str(msg.data_to_read.text) if symbol.isdigit()])
    if len(phone_number) not in range(2, texts[lang_code]["MAX_PHONE_LENGTH"] + 1):
        return None
    phone_number = "+" + phone_number
    msg.update_phone_number(phone_number)
    return phone_number


@logger_decorator_callback
def callback_to_msg(call: types.CallbackQuery) -> types.Message:
    """Extract types.Message object from types.CallbackQuery object replacing sender ID from bot's to Customer's one.

    Args:
        call: CallbackQuery object.

    Returns:
        Message object with Customer's ID in it.

    """
    call.message.from_user.id = call.from_user.id
    msg = call.message
    return msg


@logger_decorator_callback
def clear_cart(call: types.CallbackQuery) -> None:
    """Clear Customer's cart on receiving corresponding callback query.

    Args:
        call: Callback query with Customer's cart deletion request.

    """
    c_back = DBInterface(call)
    lang_code = c_back.get_customer_lang()
    callback_id = c_back.data_to_read.id
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    cus_bot.answer_callback_query(callback_id, texts[lang_code]["DELETING_CART_ALERT"], show_alert=True)
    cus_bot.delete_message(customer_id, message_id)
    c_back.delete_cart()
    show_main_menu(callback_to_msg(c_back.data_to_read))


@logger_decorator_callback
def prices_calc(call: types.CallbackQuery) -> None:
    """Calculate subtotal courier and service fees and total based on dishes in Customer's cart.

    Args:
        call: Callback query containing Customer's Telegram ID.

    """
    c_back = DBInterface(call)
    lang_code = c_back.get_customer_lang()
    dishes_uuids = c_back.get_from_cart("dishes_uuids")
    subtotal = 0
    for dish in dishes_uuids:
        c_back.data_to_read.data = dish
        dish_price = c_back.get_dish()[2]
        subtotal += dish_price
    c_back.data_to_read.data = subtotal
    c_back.add_to_cart("subtotal")
    if subtotal > 0:
        courier_fee = round(texts[lang_code]["COURIER_FEE_BASE"]
                            + float(subtotal)*texts[lang_code]["COURIER_FEE_RATE"],
                            2)
        service_fee = round(texts[lang_code]["SERVICE_FEE_BASE"]
                            + float(subtotal)*texts[lang_code]["SERVICE_FEE_RATE"],
                            2)
    else:
        courier_fee = round(0, 2)
        service_fee = round(0, 2)
    c_back.data_to_read.data = courier_fee
    c_back.add_to_cart("courier_fee")
    c_back.data_to_read.data = service_fee
    c_back.add_to_cart("service_fee")
    total = round(float(subtotal) + courier_fee + service_fee, 2)
    c_back.data_to_read.data = total
    c_back.add_to_cart("total")


# Sing in/sign up block.
@cus_bot.message_handler(commands=["start"])
@logger_decorator_msg
def start(message: types.Message) -> None:
    """Commence interaction between Customer and the bot.
    Check if Customer in the DB and start corresponding interaction sequence.

    Args:
        message: /start command from Customer.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    customer_name = msg.user_in_db()
    customer_id = msg.data_to_read.from_user.id
    msg.delete_cart()
    if customer_name:
        cus_bot.send_message(customer_id, texts[lang_code]["WELCOME_BACK_MSG"](customer_name))
        show_main_menu(msg.data_to_read)
    else:
        cus_bot.send_message(customer_id, texts[lang_code]["FIRST_WELCOME_MSG"])
        cus_bot.send_message(customer_id,
                             texts[lang_code]["ASK_AGREEMENT_MSG"],
                             reply_markup=customer_menus.agreement_menu(lang_code))


@cus_bot.message_handler(func=lambda message: message.text in [lang["SHOW_AGREEMENT_BTN"] for lang in texts.values()])
@logger_decorator_msg
def show_agreement(message: types.Message) -> None:
    """Show Customer agreement.

    Args:
        message: Show Agreement input from Customer.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    customer_id = msg.data_to_read.from_user.id
    cus_bot.send_message(customer_id, texts[lang_code]["AGREEMENT_TEXT"])


@cus_bot.message_handler(func=lambda message: message.text in [lang["ACCEPT_AGREEMENT_BTN"] for lang in texts.values()])
@logger_decorator_msg
def agreement_accepted(message: types.Message) -> None:
    """Commence Customer sign up sequence.
    Add new Customer to the DB.

    Args:
        message: Accept Agreement input from Customer.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    user = msg.user_in_db()
    customer_id = msg.data_to_read.from_user.id
    if not user:
        msg.add_customer()
    cus_bot.send_message(customer_id, texts[lang_code]["AGREEMENT_ACCEPTED_MSG"])
    cus_bot.send_message(customer_id,
                         texts[lang_code]["REG_NAME_MSG"],
                         reply_markup=types.ForceReply(
                             input_field_placeholder=texts[lang_code]["REG_NAME_PLACEHOLDER"]))


@cus_bot.message_handler(func=lambda message: message.reply_to_message \
                                              and message.reply_to_message.text \
                                              in [lang["REG_NAME_MSG"] for lang in texts.values()])
@logger_decorator_msg
def reg_name(message: types.Message) -> None:
    """Add Customer's name to the DB.
    Ask Customer to choose phone number input method.

    Args:
        message: Customer's name.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    customer_id = msg.data_to_read.from_user.id
    new_name = msg.data_to_read.text
    msg.update_name()
    cus_bot.send_message(customer_id, texts[lang_code]["REG_NAME_RECEIVED_MSG"](new_name))
    cus_bot.send_message(customer_id,
                         texts[lang_code]["REG_PHONE_METHOD_MSG"],
                         reply_markup=customer_menus.reg_phone_menu(lang_code))


@cus_bot.message_handler(content_types=["contact"])
@cus_bot.message_handler(func=lambda message: message.text in [lang["REG_PHONE_METHOD_MSG"] for lang in texts.values()])
@logger_decorator_msg
def contact(message: types.Message) -> None:
    """Add Customer's phone number imported via Telegram contact info into the DB.
    Ask Customer to provide delivery location.

    Args:
        message: Customer's Telegram contact info.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    phone_number = msg.data_to_read.contact.phone_number
    if phone_number[0] != "+":
        phone_number = "+" + phone_number
    customer_id = msg.data_to_read.from_user.id
    msg.update_phone_number(phone_number)
    cus_bot.send_message(customer_id, texts[lang_code]["PHONE_RECEIVED_MSG"](phone_number))
    cus_bot.send_message(customer_id,
                         texts[lang_code]["REG_LOCATION_MSG"],
                         reply_markup=customer_menus.reg_location_menu(lang_code))


@cus_bot.message_handler(func=lambda message: message.text in [lang["REG_PHONE_MAN_BTN"] for lang in texts.values()])
@logger_decorator_msg
def reg_phone_str(message: types.Message) -> None:
    """Ask Customer to input phone number manually.

    Args:
        message: Request form Customer to input phone number manually.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    customer_id = msg.data_to_read.from_user.id
    cus_bot.send_message(customer_id,
                         texts[lang_code]["REG_PHONE_MSG"],
                         reply_markup=types.ForceReply(
                             input_field_placeholder=texts[lang_code]["REG_PHONE_PLACEHOLDER"]
                         ))


@cus_bot.message_handler(func=lambda message: message.reply_to_message \
                                              and message.reply_to_message.text \
                                              in [lang["REG_PHONE_MSG"] for lang in texts.values()])
@logger_decorator_msg
def reg_phone(message: types.Message) -> None:
    """Check if phone number was added to the DB if manual input was chosen.
    Ask Customer to provide delivery location if so.
    Ask Customer to input phone number again otherwise.

    Args:
        message: Customer's phone number entered manually.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    customer_id = msg.data_to_read.from_user.id
    if phone_number := phone_from_msg(message):
        cus_bot.send_message(customer_id, texts[lang_code]["PHONE_RECEIVED_MSG"](phone_number))
        cus_bot.send_message(customer_id,
                             texts[lang_code]["REG_LOCATION_MSG"],
                             reply_markup=customer_menus.reg_location_menu(lang_code))
    else:
        cus_bot.send_message(customer_id, texts[lang_code]["INVALID_PHONE_MSG"])
        cus_bot.send_message(customer_id,
                             texts[lang_code]["REG_PHONE_MSG"],
                             reply_markup=types.ForceReply(
                                 input_field_placeholder=texts[lang_code]["REG_PHONE_PLACEHOLDER"]
                             ))


@cus_bot.message_handler(content_types=["location"])
@cus_bot.message_handler(func=lambda message: message.text in [lang["REG_LOCATION_BTN"] for lang in texts.values()])
@logger_decorator_msg
def reg_location(message: types.Message) -> None:
    """Add location to the DB. Proceed to main menu.

    Args:
        message: Location from Customer.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    customer_id = msg.data_to_read.from_user.id
    latitude = msg.data_to_read.location.latitude
    longitude = msg.data_to_read.location.longitude
    msg.update_customer_location()
    cus_bot.send_message(customer_id, texts[lang_code]["REG_LOCATION_RECEIVED_MSG"])
    cus_bot.send_location(customer_id, latitude, longitude)
    show_main_menu(msg.data_to_read)


# Main menu block.
@cus_bot.message_handler(func=lambda message: message.text in [lang["OPTIONS_BTN"] for lang in texts.values()])
@logger_decorator_msg
def options(message: types.Message) -> None:
    """Show options menu.

    Args:
        message: Options request from Customer.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    customer_id = msg.data_to_read.from_user.id
    cus_bot.send_message(customer_id,
                         texts[lang_code]["OPTIONS_MSG"],
                         reply_markup=customer_menus.options_menu(lang_code))


@cus_bot.message_handler(func=lambda message: message.text in [lang["MY_ORDERS_BTN"] for lang in texts.values()])
@logger_decorator_msg
def my_orders(message: types.Message) -> None:
    """Send Customer their order history.

    Args:
        message: Message from Customer with corresponding request.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    customer_id = msg.data_to_read.from_user.id
    if orders := msg.show_my_orders():
        while orders:
            cus_bot.send_message(customer_id, texts[lang_code]["MY_ORDERS_MSG"](orders))
            orders.pop(0)
        show_main_menu(msg.data_to_read)
    else:
        cus_bot.send_message(customer_id, texts[lang_code]["NO_ORDERS_FOUND_MSG"])
        show_main_menu(msg.data_to_read)


@cus_bot.message_handler(func=lambda message: message.text in [lang["NEW_ORDER_BTN"] for lang in texts.values()])
@logger_decorator_msg
def new_order(message: types.Message) -> None:
    """Commence order creation sequence.
    Check if User location is provided.
    If location is provided, ask confirmation.

    Args:
        message: Request form Customer to create new order.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    customer_id = msg.data_to_read.from_user.id
    if location := msg.check_if_location():
        cus_bot.send_message(customer_id,
                             texts[lang_code]["CONFIRM_LOCATION_MSG"],
                             reply_markup=types.ReplyKeyboardRemove())
        cus_bot.send_location(customer_id,
                              location["lat"],
                              location["lon"],
                              reply_markup=customer_menus.confirm_location_menu(lang_code))
    else:
        cus_bot.send_message(customer_id, texts[lang_code]["LOCATION_NOT_FOUND_MSG"])
        show_main_menu(msg.data_to_read)


# Options menu block.
@cus_bot.message_handler(func=lambda message: message.text in [lang["MAIN_MENU_BTN"] for lang in texts.values()])
@logger_decorator_msg
def main_menu(message: types.Message) -> None:
    """Get back to main menu.

    Args:
        message: Main menu request from Customer.

    """
    show_main_menu(message)


@cus_bot.message_handler(func=lambda message: message.text in [lang["CONTACT_SUPPORT_BTN"] for lang in texts.values()])
@logger_decorator_msg
def contact_support(message: types.Message) -> None:  # TODO Contact support.
    """Start communication with support.

    Args:
        message: Message from Customer with corresponding request.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    customer_id = msg.data_to_read.from_user.id
    cus_bot.send_message(customer_id, texts[lang_code]["IN_DEV"])
    show_main_menu(message)


@cus_bot.message_handler(func=lambda message: message.text \
                                              in [lang["RESET_CONTACT_INFO_BTN"] for lang in texts.values()])
@logger_decorator_msg
def reset_contact_info(message: types.Message) -> None:
    """Ask Customer for contact info reset confirmation.

    Args:
        message: Request form Customer to reset contact info.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    customer_id = msg.data_to_read.from_user.id
    cus_bot.send_message(customer_id,
                         texts[lang_code]["RESET_CONTACT_INFO_MSG"],
                         reply_markup=customer_menus.reset_info_menu(lang_code))


@cus_bot.message_handler(func=lambda message: message.text in [lang["DELETE_PROFILE_BTN"] for lang in texts.values()])
@logger_decorator_msg
def delete_profile(message: types.Message) -> None:
    """Ask Customer for profile deletion confirmation.

    Args:
        message: Deletion request from Customer.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    customer_id = msg.data_to_read.from_user.id
    cus_bot.send_message(customer_id,
                         texts[lang_code]["DELETE_PROFILE_MSG"],
                         reply_markup=customer_menus.confirm_delete_profile_menu(lang_code))


# Language change menu.
@cus_bot.message_handler(func=lambda message: message.text in [lang["CHANGE_LANG_BTN"] for lang in texts.values()])
@logger_decorator_msg
def change_lang_menu(message: types.Message) -> None:
    """Open language select menu.

    Args:
        message: Message from Customer with corresponding request.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    customer_id = msg.data_to_read.from_user.id
    cus_bot.send_message(customer_id, texts[lang_code]["LANG_SEL_MENU"], reply_markup=types.ReplyKeyboardRemove())
    cus_bot.send_message(customer_id,
                         texts[lang_code]["CHANGE_LANG_MSG"],
                         reply_markup=customer_menus.lang_sel_menu(lang_code))


@cus_bot.callback_query_handler(func=lambda call: call.message.text \
                                                  in [lang["CHANGE_LANG_MSG"] for lang in texts.values()])
@logger_decorator_callback
def lang_set(call: types.CallbackQuery) -> None:
    """Change bot interface language.

    Args:
        call: Callback query from Customer with selected language info.

    """
    c_back = DBInterface(call)
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    c_back.set_customer_lang()
    cus_bot.delete_message(customer_id, message_id - 1)
    cus_bot.delete_message(customer_id, message_id)
    show_main_menu(callback_to_msg(c_back.data_to_read))


# Contact Info reset block.
@cus_bot.message_handler(func=lambda message: message.text in [lang["CONFIRM_RESET_BTN"] for lang in texts.values()])
@logger_decorator_msg
def confirm_reset(message: types.Message) -> None:
    """Commence contact info reset sequence.

    Args:
        message: Confirmation from Customer.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    customer_id = msg.data_to_read.from_user.id
    msg.delete_customer()
    cus_bot.send_message(customer_id, texts[lang_code]["CONTACT_INFO_DELETED_MSG"])
    agreement_accepted(message)


# Profile deletion block.
@cus_bot.message_handler(func=lambda message: message.text \
                                              in [lang["CONFIRM_DELETE_PROFILE_BTN"] for lang in texts.values()])
@logger_decorator_msg
def confirm_delete(message: types.Message) -> None:
    """Delete Customer's profile from DB.

    Args:
        message: Confirmation from Customer.

    """
    msg = DBInterface(message)
    lang_code = msg.get_customer_lang()
    customer_id = msg.data_to_read.from_user.id
    msg.delete_customer()
    cus_bot.send_message(customer_id, texts[lang_code]["PROFILE_DELETED_MSG"], reply_markup=types.ReplyKeyboardRemove())


# Creating order sequence block.
@cus_bot.callback_query_handler(func=lambda call: call.message.location)
@logger_decorator_callback
def check_location_confirmation(call: types.CallbackQuery) -> None:
    """Process Customer's response to location confirmation request.
    Show Customer restaurant type selection menu if confirmed,
    send back to main menu if not.

    Args:
        call: Callback query from Customer with response to location confirmation request.

    """
    c_back = DBInterface(call)
    lang_code = c_back.get_customer_lang()
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    callback_data = c_back.data_to_read.data
    cus_bot.delete_message(customer_id, message_id)
    cus_bot.delete_message(customer_id, message_id - 1)
    if callback_data == texts[lang_code]["WRONG_LOCATION_BTN"]:
        cus_bot.send_message(customer_id, texts[lang_code]["REQUEST_NEW_LOCATION_MSG"])
        show_main_menu(callback_to_msg(c_back.data_to_read))
    elif callback_data == texts[lang_code]["CONFIRM_LOCATION_BTN"]:
        c_back.new_cart()
        cus_bot.send_message(customer_id,
                             texts[lang_code]["CHOOSE_REST_TYPE_MSG"],
                             reply_markup=customer_menus.choose_rest_type_menu(lang_code))


@cus_bot.callback_query_handler(func=lambda call: call.message.text \
                                                  in [lang["CHOOSE_REST_TYPE_MSG"] for lang in texts.values()])
@logger_decorator_callback
def rest_type_chosen(call: types.CallbackQuery) -> None:
    """Process Customer's response to restaurant type selection.
    Show Customer restaurants of selected type
    and add restaurant type to the Customer's cart
    or go back to main menu if "go back" button is clicked.
    
    Args:
        call: Callback query from Customer with response to restaurant type selection.

    """
    c_back = DBInterface(call)
    lang_code = c_back.get_customer_lang()
    callback_data = c_back.data_to_read.data
    callback_id = c_back.data_to_read.id
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    if callback_data == customer_menus.back_button(lang_code).callback_data:
        cus_bot.answer_callback_query(callback_id, texts[lang_code]["EXITING_ORDER_MENU_MSG"])
        cus_bot.delete_message(customer_id, message_id)
        c_back.delete_cart()
        show_main_menu(callback_to_msg(c_back.data_to_read))
    else:
        c_back.add_to_cart("restaurant_type")
        cus_bot.edit_message_text(texts[lang_code]["REST_TYPE_SELECTED_MSG"](callback_data), customer_id, message_id)
        cus_bot.send_message(customer_id,
                             texts[lang_code]["CHOOSE_REST_MSG"],
                             reply_markup=customer_menus.choose_rest_menu(lang_code, c_back))


@cus_bot.callback_query_handler(func=lambda call: call.message.text \
                                                  in [lang["CHOOSE_REST_MSG"] for lang in texts.values()])
@logger_decorator_callback
def restaurant_chosen(call: types.CallbackQuery) -> None:
    """Process Customer's response to restaurant selection.
    Show Customer dish types available in selected restaurant
    and add restaurant UUID to the Customer's cart
    or go back to main menu if "go back" button is clicked.

    Args:
        call: Callback query from Customer with response to restaurant selection.

    """
    c_back = DBInterface(call)
    lang_code = c_back.get_customer_lang()
    callback_data = c_back.data_to_read.data
    callback_id = c_back.data_to_read.id
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    try:
        cus_bot.delete_message(customer_id, message_id - 1)
    except ApiTelegramException:
        pass
    if callback_data == customer_menus.back_button(lang_code).callback_data:
        cus_bot.answer_callback_query(callback_id, texts[lang_code]["DELETING_CART_ALERT"], show_alert=True)
        cus_bot.delete_message(customer_id, message_id)
        c_back.delete_cart()
        show_main_menu(callback_to_msg(c_back.data_to_read))
    else:
        c_back.add_to_cart("restaurant_uuid")
        restaurant = c_back.rest_name_by_uuid()
        cus_bot.edit_message_text(texts[lang_code]["REST_SELECTED_MSG"](restaurant), customer_id, message_id)
        cus_bot.send_message(customer_id,
                             texts[lang_code]["CHOOSE_DISH_CATEGORY_MSG"],
                             reply_markup=customer_menus.choose_dish_cat_menu(lang_code, c_back))


@cus_bot.callback_query_handler(func=lambda call: call.message.text \
                                                  in [lang["CHOOSE_DISH_CATEGORY_MSG"] for lang in texts.values()])
@logger_decorator_callback
def dish_category_chosen(call: types.CallbackQuery) -> None:
    """Process Customer's response to dish category selection.
    Show Customer dishes of selected category available in selected restaurant
    or go back to restaurant selection menu if "go back" button is clicked.
    Show Customer their cart or clear it if corresponding buttons are clicked.

    Args:
        call: Callback query from Customer with response to dish category selection.

    """
    c_back = DBInterface(call)
    lang_code = c_back.get_customer_lang()
    callback_data = c_back.data_to_read.data
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    try:
        cus_bot.delete_message(customer_id, message_id - 1)
    except ApiTelegramException:
        pass
    if callback_data == customer_menus.back_button(lang_code).callback_data:
        c_back.delete_from_cart("restaurant_uuid")
        c_back.data_to_read.data = c_back.get_from_cart("restaurant_type")
        rest_type_chosen(c_back.data_to_read)
    elif callback_data == customer_menus.cancel_order_button(lang_code).callback_data:
        clear_cart(c_back.data_to_read)
    elif callback_data == customer_menus.cart_button(lang_code).callback_data:
        is_dish_added(c_back.data_to_read)
    else:
        cus_bot.edit_message_text(texts[lang_code]["DISH_CAT_SELECTED_MSG"](c_back.data_to_read.data),
                                  customer_id,
                                  message_id)
        cus_bot.send_message(customer_id,
                             texts[lang_code]["CHOOSE_DISH_MSG"],
                             reply_markup=customer_menus.choose_dish_menu(lang_code, c_back))


@cus_bot.callback_query_handler(func=lambda call: call.message.text \
                                                  in [lang["CHOOSE_DISH_MSG"] for lang in texts.values()])
@logger_decorator_callback
def dish_chosen(call: types.CallbackQuery) -> None:
    """Process Customer's response to dish selection.
    Show Customer dish selection confirmation menu displaying dish description and price
    or go back to restaurant selection menu if "go back" button is clicked.
    Show Customer their cart or clear it if corresponding buttons are clicked.

    Args:
        call: Callback query from Customer with response to dish selection.

    """
    c_back = DBInterface(call)
    lang_code = c_back.get_customer_lang()
    callback_data = c_back.data_to_read.data
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    try:
        cus_bot.delete_message(customer_id, message_id - 1)
    except ApiTelegramException:
        pass
    if callback_data == customer_menus.back_button(lang_code).callback_data:
        rest_uuid = c_back.get_from_cart("restaurant_uuid")
        c_back.data_to_read.data = rest_uuid
        restaurant_chosen(c_back.data_to_read)
    elif callback_data == customer_menus.cancel_order_button(lang_code).callback_data:
        clear_cart(c_back.data_to_read)
    elif callback_data == customer_menus.cart_button(lang_code).callback_data:
        is_dish_added(c_back.data_to_read)
    else:
        cus_bot.edit_message_text(texts[lang_code]["DISH_SELECTED_MSG"](c_back.get_dish()),
                                  customer_id,
                                  message_id)
        cus_bot.send_message(customer_id,
                             texts[lang_code]["ADD_DISH_MSG"],
                             reply_markup=customer_menus.conf_sel_dish_menu(lang_code, c_back))


@cus_bot.callback_query_handler(func=lambda call: call.message.text \
                                                  in [lang["ADD_DISH_MSG"] for lang in texts.values()])
@logger_decorator_callback
def is_dish_added(call: types.CallbackQuery) -> None:
    """Process Customer's response to selected dish confirmation.
    Show Customer's cart menu displaying dishes and price
    or go back to dish category selection menu if confirmation isn't obtained.

    Args:
        call: Callback query from Customer with response to selected dish confirmation.

    """
    c_back = DBInterface(call)
    lang_code = c_back.get_customer_lang()
    callback_data = c_back.data_to_read.data
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    try:
        cus_bot.delete_message(customer_id, message_id - 1)
    except ApiTelegramException:
        pass
    if callback_data == customer_menus.back_button(lang_code).callback_data:
        rest_uuid = c_back.get_from_cart("restaurant_uuid")
        c_back.data_to_read.data = rest_uuid
        restaurant_chosen(c_back.data_to_read)
    else:
        if callback_data != customer_menus.cart_button(lang_code).callback_data:
            new_c_back = DBInterface(call)
            dishes_uuids = c_back.get_from_cart("dishes_uuids")
            if not dishes_uuids:
                dishes_uuids = []
            dishes_uuids.append(callback_data)
            new_c_back.data_to_read.data = dishes_uuids
            new_c_back.add_to_cart("dishes_uuids")
            prices_calc(new_c_back.data_to_read)
        c_back.data_to_read.data = c_back.get_from_cart("dishes_uuids")
        dishes = []
        if c_back.data_to_read.data:
            for dish in c_back.data_to_read.data:
                c_back.data_to_read.data = dish
                dish_name = c_back.get_dish()[0]
                dishes.append(dish_name)
        dishes_displayed = "\n".join(sorted(dishes))
        subtotal = c_back.get_from_cart("subtotal")
        courier_fee = c_back.get_from_cart("courier_fee")
        service_fee = c_back.get_from_cart("service_fee")
        total = c_back.get_from_cart("total")
        cart_text = texts[lang_code]["YOUR_CART_MSG"](dishes_displayed,
                                                      subtotal,
                                                      courier_fee,
                                                      service_fee,
                                                      total)
        cus_bot.edit_message_text(cart_text, customer_id, message_id)
        cus_bot.send_message(customer_id,
                             texts[lang_code]["CART_ACTIONS_MSG"],
                             reply_markup=customer_menus.cart_menu(lang_code))


@cus_bot.callback_query_handler(func=lambda call: call.message.text \
                                                  in [lang["CART_ACTIONS_MSG"] for lang in texts.values()])
@logger_decorator_callback
def cart_actions(call: types.CallbackQuery) -> None:
    """Process Customer's input from cart actions menu.
    Clear cart if corresponding button is clicked.
    Call item deletion menu on request.
    Return Customer to dish category selection menu on request.
    Proceed to payment menu on request.

    Args:
        call: Callback query with Customer's input from cart actions menu.

    """
    c_back = DBInterface(call)
    lang_code = c_back.get_customer_lang()
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    cus_bot.delete_message(customer_id, message_id - 1)
    if c_back.data_to_read.data == customer_menus.cancel_order_button(lang_code).callback_data:
        clear_cart(c_back.data_to_read)
    elif c_back.data_to_read.data == texts[lang_code]["DELETE_ITEM_BTN"]:
        cus_bot.edit_message_text(texts[lang_code]["DELETE_ITEM_MSG"],
                                  customer_id,
                                  message_id,
                                  reply_markup=customer_menus.item_deletion_menu(lang_code, c_back))
    elif c_back.data_to_read.data == texts[lang_code]["ADD_MORE_BTN"]:
        c_back.data_to_read.data = c_back.get_from_cart("restaurant_uuid")
        c_back.data_to_read.message.text = texts[lang_code]["ADD_MORE_BTN"]
        restaurant_chosen(c_back.data_to_read)
    elif c_back.data_to_read.data == texts[lang_code]["MAKE_ORDER_BTN"]:
        order_info = c_back.order_creation()
        cus_bot.edit_message_text(texts[lang_code]["ORDER_CREATED_MSG"](order_info), customer_id, message_id)
        cus_bot.send_message(customer_id,
                             texts[lang_code]["PAYMENT_MENU_MSG"],
                             reply_markup=customer_menus.payment_menu(lang_code, order_info[0]))


@cus_bot.callback_query_handler(func=lambda call: call.message.text \
                                                  in [lang["DELETE_ITEM_MSG"] for lang in texts.values()])
@logger_decorator_callback
def item_deletion(call: types.CallbackQuery) -> None:
    """Delete selected item from Customer's cart.
    Call cart menu.

    Args:
        call: Callback query with Customer's input from item deletion menu.

    """
    c_back = DBInterface(call)
    lang_code = c_back.get_customer_lang()
    if c_back.data_to_read.data != customer_menus.cart_button(lang_code).callback_data:
        if dishes_uuids := c_back.get_from_cart("dishes_uuids"):
            dishes_uuids.remove(c_back.data_to_read.data)
            c_back.data_to_read.data = dishes_uuids
            c_back.add_to_cart("dishes_uuids")
        prices_calc(c_back.data_to_read)
    c_back.data_to_read.data = customer_menus.cart_button(lang_code).callback_data
    is_dish_added(c_back.data_to_read)


# Payment block.
@cus_bot.callback_query_handler(func=lambda call: "paid" in call.data)
@logger_decorator_callback
def order_paid(call: types.CallbackQuery) -> None:
    """Process "paid" button,
    Send payment confirmation request to Admin.

    Args:
        call: Callback query from "paid" button with order UUID in it.

    """
    c_back = DBInterface(call)
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    lang_code = c_back.get_customer_lang()
    admin_id = c_back.get_support_id()
    adm_lang_code = c_back.get_adm_lang(admin_id)
    order_uuid = c_back.data_to_read.data.split(maxsplit=1)[1]
    total = c_back.get_order_info(order_uuid, "total")
    adm_bot.send_message(admin_id,
                         texts[adm_lang_code]["PAID_ADM_MSG"](order_uuid, total),
                         reply_markup=customer_menus.adm_pay_conf_menu(adm_lang_code, order_uuid))
    cus_bot.edit_message_text(texts[lang_code]["WAIT_FOR_CONFIRMATION_MSG"](order_uuid), customer_id, message_id)
    c_back.delete_cart()
    show_main_menu(callback_to_msg(c_back.data_to_read))


@cus_bot.callback_query_handler(func=lambda call: "order_closed" in call.data)
@logger_decorator_callback
def order_closed(call: types.CallbackQuery) -> None:
    """Process confirmation of order receiving from Customer.

    Args:
        call: Callback query from "Order received" button with order UUID in it.

    """
    c_back = DBInterface(call)
    order_uuid = c_back.data_to_read.data.split(maxsplit=1)[-1]
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    lang_code = c_back.get_customer_lang()
    c_back.close_order()
    cus_bot.edit_message_reply_markup(customer_id, message_id)
    cus_bot.send_message(customer_id, texts[lang_code]["ORDER_CLOSED_MSG"](order_uuid))


@cus_bot.callback_query_handler(func=lambda call: "cancel" in call.data)
@logger_decorator_callback
def cancel(call: types.CallbackQuery) -> None:
    """Process order cancellation button after order is already created.

    Args:
        call: Callback query from "Cancel order" button with order UUID in it.

    """
    c_back = DBInterface(call)
    order_uuid = c_back.data_to_read.data.split(maxsplit=1)[-1]
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    lang_code = c_back.get_customer_lang()
    c_back.delete_cart()
    c_back.delete_order()
    cus_bot.edit_message_text(texts[lang_code]["CANCEL_MSG"](order_uuid), customer_id, message_id)
    show_main_menu(callback_to_msg(c_back.data_to_read))


def main():
    logger.info("The bot is running.")
    cus_bot.infinity_polling()


if __name__ == "__main__":
    main()
