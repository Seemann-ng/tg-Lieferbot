import telebot as tb
import telebot.types as types
from environs import Env

import customermenus
from loggertool import logger, logger_decorator_callback, logger_decorator_msg
from customerdbtools import Interface as DBInterface

env = Env()
env.read_env()

BOT_TOKEN = env.str("CUSTOMER_BOT_TOKEN")

bot = tb.TeleBot(token=BOT_TOKEN)


# Auxiliary functions.
@logger_decorator_msg
def show_main_menu(message: types.Message) -> None:
    """Show Customer main menu if Customer is in the DB, otherwise call start().

    Args:
        message: Main menu request from Customer.

    """
    msg = DBInterface(message)
    if msg.user_in_db():
        customer_id = msg.data_to_read.from_user.id
        bot.send_message(customer_id, customermenus.MAIN_MENU_MSG, reply_markup=customermenus.main_menu)
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
    phone_number = str(msg.data_to_read.text)
    for symbol in phone_number:
        if not symbol.isdigit():
            phone_number = phone_number.replace(symbol, "")
    if len(phone_number) not in range(2, customermenus.MAX_PHONE_LENGTH_WO_PREFIX + 1):
        return None
    else:
        phone_number = f"{customermenus.PHONE_NUM_PREFIX}" + phone_number
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
    callback_id = c_back.data_to_read.id
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    bot.answer_callback_query(callback_id, customermenus.DELETING_CART_ALERT, show_alert=True)
    bot.delete_message(customer_id, message_id)
    c_back.delete_cart()
    show_main_menu(callback_to_msg(c_back.data_to_read))


@logger_decorator_callback
def prices_calc(call: types.CallbackQuery) -> None:
    """Calculate subtotal courier and service fees and total based on dishes in Customer's cart.

    Args:
        call: Callback query containing Customer's Telegram ID.

    """
    c_back = DBInterface(call)
    dishes_uuids = c_back.get_from_cart("dishes_uuids")
    subtotal = 0
    for dish in dishes_uuids:
        c_back.data_to_read.data = dish
        dish_price = c_back.get_dish()[2]
        subtotal += dish_price
    c_back.data_to_read.data = subtotal
    c_back.add_to_cart("subtotal")
    if subtotal > 0:
        courier_fee = round(customermenus.COURIER_FEE_BASE + float(subtotal) * customermenus.COURIER_FEE_RATE, 2)
        service_fee = round(customermenus.SERVICE_FEE_BASE + float(subtotal) * customermenus.SERVICE_FEE_RATE, 2)
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
@bot.message_handler(commands=["start"])
@logger_decorator_msg
def start(message: types.Message) -> None:
    """Commence interaction between Customer and the bot.
    Check if Customer in the DB and start corresponding interaction sequence.

    Args:
        message: /start command from Customer.

    """
    msg = DBInterface(message)
    customer_name = msg.user_in_db()
    customer_id = msg.data_to_read.from_user.id
    msg.delete_cart()
    if customer_name:
        bot.send_message(customer_id, customermenus.WELCOME_BACK_MSG + customer_name)
        show_main_menu(msg.data_to_read)
    else:
        bot.send_message(customer_id, customermenus.FIRST_WELCOME_MSG)
        bot.send_message(customer_id, customermenus.ASK_AGREEMENT_MSG, reply_markup=customermenus.agreement_menu)


@bot.message_handler(regexp=customermenus.SHOW_AGREEMENT_BTN)
@logger_decorator_msg
def show_agreement(message: types.Message) -> None:
    """Show Customer agreement.

    Args:
        message: Show Agreement input from Customer.

    """
    bot.send_message(message.from_user.id, customermenus.AGREEMENT_TEXT)


@bot.message_handler(regexp=customermenus.ACCEPT_AGREEMENT_BTN)
@logger_decorator_msg
def agreement_accepted(message: types.Message) -> None:
    """Commence Customer sign up sequence.
    Add new Customer to the DB.

    Args:
        message: Accept Agreement input from Customer.

    """
    msg = DBInterface(message)
    user = msg.user_in_db()
    customer_id = msg.data_to_read.from_user.id
    if not user:
        msg.add_customer()
    bot.send_message(customer_id, customermenus.AGREEMENT_ACCEPTED_MSG)
    bot.send_message(customer_id,
                     customermenus.REG_NAME_MSG,
                     reply_markup=types.ForceReply(input_field_placeholder=customermenus.REG_NAME_PLACEHOLDER))


@bot.message_handler(func=lambda message: message.reply_to_message\
                                          and message.reply_to_message.text == customermenus.REG_NAME_MSG)
@logger_decorator_msg
def reg_name(message: types.Message) -> None:
    """Add Customer's name to the DB.
    Ask Customer to choose phone number input method.

    Args:
        message: Customer's name.

    """
    msg = DBInterface(message)
    customer_id = msg.data_to_read.from_user.id
    new_name = msg.data_to_read.text
    msg.update_name()
    bot.send_message(customer_id,
                     customermenus.REG_NAME_RECEIVED_MSG + new_name)
    bot.send_message(customer_id,
                     customermenus.REG_PHONE_METHOD_MSG,
                     reply_markup=customermenus.reg_phone_menu)


@bot.message_handler(content_types=["contact"])
@bot.message_handler(regexp=customermenus.REG_PHONE_METHOD_MSG)
@logger_decorator_msg
def contact(message: types.Message) -> None:
    """Add Customer's phone number imported via Telegram contact info into the DB.
    Ask Customer to provide delivery location.

    Args:
        message: Customer's Telegram contact info.

    """
    msg = DBInterface(message)
    phone_number = msg.data_to_read.contact.phone_number
    customer_id = msg.data_to_read.from_user.id
    msg.update_phone_number(phone_number)
    bot.send_message(customer_id,
                     customermenus.PHONE_RECEIVED_MSG + phone_number)
    bot.send_message(customer_id,
                     customermenus.REG_LOCATION_MSG,
                     reply_markup=customermenus.reg_location_menu)


@bot.message_handler(regexp=customermenus.REG_PHONE_MAN_BTN)
@logger_decorator_msg
def reg_phone_str(message: types.Message) -> None:
    """Ask Customer to input phone number manually.

    Args:
        message: Request form Customer to input phone number manually.

    """
    bot.send_message(message.from_user.id,
                     customermenus.REG_PHONE_MSG,
                     reply_markup=types.ForceReply(input_field_placeholder=customermenus.REG_PHONE_PLACEHOLDER))


@bot.message_handler(func=lambda message: message.reply_to_message\
                                          and message.reply_to_message.text == customermenus.REG_PHONE_MSG)
@logger_decorator_msg
def reg_phone(message: types.Message) -> None:
    """Check if phone number was added to the DB if manual input was chosen.
    Ask Customer to provide delivery location if so.
    Ask Customer to input phone number again otherwise.

    Args:
        message: Customer's phone number entered manually.

    """
    phone_number = phone_from_msg(message)
    if not phone_number:
        bot.send_message(message.from_user.id,
                         customermenus.INVALID_PHONE_MSG)
        bot.send_message(message.from_user.id,
                         customermenus.REG_PHONE_MSG,
                         reply_markup=types.ForceReply(input_field_placeholder=customermenus.REG_PHONE_PLACEHOLDER))
    else:
        bot.send_message(message.from_user.id,
                         customermenus.PHONE_RECEIVED_MSG + phone_number)
        bot.send_message(message.from_user.id,
                         customermenus.REG_LOCATION_MSG,
                         reply_markup=customermenus.reg_location_menu)


@bot.message_handler(content_types=["location"])
@bot.message_handler(regexp=customermenus.REG_LOCATION_BTN)
@logger_decorator_msg
def reg_location(message: types.Message) -> None:
    """Add location to the DB. Proceed to main menu.

    Args:
        message: Location from Customer.

    """
    msg = DBInterface(message)
    latitude = msg.data_to_read.location.latitude
    longitude = msg.data_to_read.location.longitude
    msg.update_customer_location()
    bot.send_message(message.from_user.id,
                     customermenus.REG_LOCATION_RECEIVED_MSG)
    bot.send_location(message.from_user.id,
                      latitude,
                      longitude)
    show_main_menu(msg.data_to_read)


# Main menu block.
@bot.message_handler(regexp=customermenus.OPTIONS_BTN)
@logger_decorator_msg
def options(message: types.Message) -> None:
    """Show options menu.

    Args:
        message: Options request from Customer.

    """
    bot.send_message(message.from_user.id,
                     customermenus.OPTIONS_MSG,
                     reply_markup=customermenus.options_menu)


@bot.message_handler(regexp=customermenus.MY_ORDERS_BTN)
@logger_decorator_msg
def my_orders(message: types.Message) -> None:
    """Send Customer their order history.

    Args:
        message: Message from Customer with corresponding request.

    """
    msg = DBInterface(message)
    orders = msg.show_my_orders()
    customer_id = msg.data_to_read.from_user.id
    if not orders:
        bot.send_message(customer_id,
                         customermenus.NO_ORDERS_FOUND_MSG)
        show_main_menu(msg.data_to_read)
    else:
        while orders:
            bot.send_message(customer_id,
                             customermenus.my_orders_msg(orders))
        show_main_menu(msg.data_to_read)


@bot.message_handler(regexp=customermenus.NEW_ORDER_BTN)
@logger_decorator_msg
def new_order(message: types.Message) -> None:
    """Commence order creation sequence.
    Check if User location is provided.
    If location is provided, ask confirmation.

    Args:
        message: Request form Customer to create new order.

    """
    msg = DBInterface(message)
    location = msg.check_if_location()
    customer_id = msg.data_to_read.from_user.id
    if not location:
        bot.send_message(customer_id,
                         customermenus.LOCATION_NOT_FOUND_MSG)
        show_main_menu(msg.data_to_read)
    else:
        bot.send_message(customer_id,
                         customermenus.CONFIRM_LOCATION_MSG,
                         reply_markup=types.ReplyKeyboardRemove())
        bot.send_location(customer_id,
                          location["lat"],
                          location["lon"],
                          reply_markup=customermenus.confirm_location_menu)


# Options menu block.
@bot.message_handler(regexp=customermenus.MAIN_MENU_BTN)
@logger_decorator_msg
def main_menu(message: types.Message) -> None:
    """Get back to main menu.

    Args:
        message: Main menu request from Customer.

    """
    show_main_menu(message)


@bot.message_handler(regexp=customermenus.CONTACT_SUPPORT_BTN)
@logger_decorator_msg
def contact_support(message: types.Message) -> None:  # TODO Contact support.
    """Start communication with support.

    Args:
        message: Message from Customer with corresponding request.

    """
    bot.send_message(message.from_user.id, customermenus.IN_DEV)
    show_main_menu(message)


@bot.message_handler(regexp=customermenus.RESET_CONTACT_INFO_BTN)
@logger_decorator_msg
def reset_contact_info(message: types.Message) -> None:
    """Ask Customer for contact info reset confirmation.

    Args:
        message: Request form Customer to reset contact info.

    """
    bot.send_message(message.from_user.id,
                     customermenus.RESET_CONTACT_INFO_MSG,
                     reply_markup=customermenus.reset_info_menu)


@bot.message_handler(regexp=customermenus.DELETE_PROFILE_BTN)
@logger_decorator_msg
def delete_profile(message: types.Message) -> None:
    """Ask Customer for profile deletion confirmation.

    Args:
        message: Deletion request from Customer.

    """
    bot.send_message(message.from_user.id,
                     customermenus.DELETE_PROFILE_MSG,
                     reply_markup=customermenus.confirm_delete_profile_menu)


# Contact Info reset block.
@bot.message_handler(regexp=customermenus.CONFIRM_RESET_BTN)
@logger_decorator_msg
def confirm_reset(message: types.Message) -> None:
    """Commence contact info reset sequence.

    Args:
        message: Confirmation from Customer.

    """
    msg = DBInterface(message)
    customer_id = msg.data_to_read.from_user.id
    msg.delete_customer()
    bot.send_message(customer_id,
                     customermenus.CONTACT_INFO_DELETED_MSG)
    agreement_accepted(message)


# Profile deletion block.
@bot.message_handler(regexp=customermenus.CONFIRM_DELETE_PROFILE_BTN)
@logger_decorator_msg
def confirm_delete(message: types.Message) -> None:
    """Delete Customer's profile from DB.

    Args:
        message: Confirmation from Customer.

    """
    msg = DBInterface(message)
    customer_id = msg.data_to_read.from_user.id
    msg.delete_customer()
    bot.send_message(customer_id,
                     customermenus.PROFILE_DELETED_MSG,
                     reply_markup=types.ReplyKeyboardRemove())


# Creating order sequence block.
@bot.callback_query_handler(func=lambda call: call.message.location)
@logger_decorator_callback
def check_location_confirmation(call: types.CallbackQuery) -> None:
    """Process Customer's response to location confirmation request.
    Show Customer restaurant type selection menu if confirmed,
    send back to main menu if not.

    Args:
        call: Callback query from Customer with response to location confirmation request.

    """
    c_back = DBInterface(call)
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    callback_data = c_back.data_to_read.data
    bot.delete_message(customer_id,
                       message_id)
    bot.delete_message(customer_id,
                       message_id - 1)
    if callback_data == customermenus.WRONG_LOCATION_MSG:
        bot.send_message(customer_id,
                         customermenus.REQUEST_NEW_LOCATION_MSG)
        show_main_menu(callback_to_msg(c_back.data_to_read))
    elif callback_data == customermenus.CONFIRM_LOCATION_BTN:
        c_back.new_cart()
        restaurant_types = DBInterface.show_restaurant_types()
        menu = types.InlineKeyboardMarkup(row_width=1)
        if restaurant_types:
            for restaurant_type in restaurant_types:
                menu.add(types.InlineKeyboardButton(text=restaurant_type[0], callback_data=restaurant_type[0]))
        menu.add(customermenus.back_button)
        bot.send_message(customer_id,
                         customermenus.CHOOSE_REST_TYPE_MSG,
                         reply_markup=menu)


@bot.callback_query_handler(func=lambda call: call.message.text == customermenus.CHOOSE_REST_TYPE_MSG)
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
    callback_data = c_back.data_to_read.data
    callback_id = c_back.data_to_read.id
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    if callback_data == customermenus.back_button.callback_data:
        bot.answer_callback_query(callback_id,
                                  customermenus.EXITING_ORDER_MENU_MSG)
        bot.delete_message(customer_id,
                           message_id)
        c_back.delete_cart()
        show_main_menu(callback_to_msg(c_back.data_to_read))
    else:
        c_back.add_to_cart("restaurant_type")
        restaurants = c_back.show_restaurants()
        menu = types.InlineKeyboardMarkup(row_width=1)
        if restaurants:
            for restaurant in restaurants:
                menu.add(types.InlineKeyboardButton(text=restaurant[0], callback_data=restaurant[1]))
        menu.add(customermenus.back_button)
        bot.edit_message_text(customermenus.SELECTED_REST_TYPE_MSG  # TODO -> customer_bot_textes as lamda
                              + f"\n{callback_data}\n"
                              + customermenus.CHOOSE_REST_MSG,
                              customer_id,
                              message_id,
                              reply_markup=menu)


@bot.callback_query_handler(func=lambda call: customermenus.CHOOSE_REST_MSG in call.message.text)
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
    callback_data = c_back.data_to_read.data
    callback_id = c_back.data_to_read.id
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    if callback_data == customermenus.back_button.callback_data:
        bot.answer_callback_query(callback_id,
                                  customermenus.DELETING_CART_ALERT,
                                  show_alert=True)
        bot.delete_message(customer_id,
                           message_id)
        c_back.delete_cart()
        show_main_menu(callback_to_msg(c_back.data_to_read))
    else:
        c_back.add_to_cart("restaurant_uuid")
        dish_categories = c_back.show_dish_categories()
        menu = types.InlineKeyboardMarkup(row_width=1)
        if dish_categories:
            for category in dish_categories:
                menu.add(types.InlineKeyboardButton(text=category[0], callback_data=category[0]))
        menu.add(customermenus.cart_button)
        if c_back.data_to_read.message.text != customermenus.ADD_MORE_BTN:
            menu.add(customermenus.back_button)
        menu.add(customermenus.cancel_order_button)
        restaurant = c_back.rest_name_by_uuid()
        bot.edit_message_text(customermenus.SELECTED_REST_MSG
                              + f"\n{restaurant}\n"
                              + customermenus.CHOOSE_DISH_CATEGORY_MSG,
                              customer_id,
                              message_id,
                              reply_markup=menu)


@bot.callback_query_handler(func=lambda call: customermenus.CHOOSE_DISH_CATEGORY_MSG in call.message.text)
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
    callback_data = c_back.data_to_read.data
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    if callback_data == customermenus.back_button.callback_data:
        c_back.delete_from_cart("restaurant_uuid")
        c_back.data_to_read.data = c_back.get_from_cart("restaurant_type")
        rest_type_chosen(c_back.data_to_read)
    elif callback_data == customermenus.cancel_order_button.callback_data:
        clear_cart(c_back.data_to_read)
    elif callback_data == customermenus.cart_button.callback_data:
        is_dish_added(c_back.data_to_read)
    else:
        dishes = c_back.show_dishes()
        menu = types.InlineKeyboardMarkup(row_width=1)
        if dishes:
            for dish in dishes:
                menu.add(types.InlineKeyboardButton(text=dish[0], callback_data=dish[1]))
        menu.add(customermenus.cart_button)
        menu.add(customermenus.back_button)
        menu.add(customermenus.cancel_order_button)
        bot.edit_message_text(customermenus.SELECTED_DISH_CAT_MSG
                              + f"\n{c_back.data_to_read.data}\n"
                              + customermenus.CHOOSE_DISH_MSG,
                              customer_id,
                              message_id,
                              reply_markup=menu)


@bot.callback_query_handler(func=lambda call: customermenus.CHOOSE_DISH_MSG in call.message.text)
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
    callback_data = c_back.data_to_read.data
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    if callback_data == customermenus.back_button.callback_data:
        rest_uuid = c_back.get_from_cart("restaurant_uuid")
        c_back.data_to_read.data = rest_uuid
        restaurant_chosen(c_back.data_to_read)
    elif callback_data == customermenus.cancel_order_button.callback_data:
        clear_cart(c_back.data_to_read)
    elif callback_data == customermenus.cart_button.callback_data:
        is_dish_added(c_back.data_to_read)
    else:
        add_dish_button = types.InlineKeyboardButton(text=customermenus.ADD_DISH_BTN,
                                                     callback_data=c_back.data_to_read.data)
        menu = types.InlineKeyboardMarkup(row_width=2)
        menu.add(customermenus.back_button, add_dish_button)
        dish = c_back.get_dish()
        new_text = "\n".join([customermenus.SELECTED_DISH_MSG,
                              f"{dish[0]}",
                              customermenus.DISH_DESC_MSG,
                              f"{dish[1]}",
                              customermenus.DISH_PRICE_MSG,
                              f"{customermenus.CURRENCY}{dish[2]}"])
        bot.edit_message_text(new_text,
                              customer_id,
                              message_id,
                              reply_markup=menu)


@bot.callback_query_handler(func=lambda call: customermenus.SELECTED_DISH_MSG in call.message.text)
@logger_decorator_callback
def is_dish_added(call: types.CallbackQuery) -> None:
    """Process Customer's response to selected dish confirmation.
    Show Customer's cart menu displaying dishes and price
    or go back to dish category selection menu if confirmation isn't obtained.

    Args:
        call: Callback query from Customer with response to selected dish confirmation.

    """
    c_back = DBInterface(call)
    callback_data = c_back.data_to_read.data
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    if callback_data == customermenus.back_button.callback_data:
        rest_uuid = c_back.get_from_cart("restaurant_uuid")
        c_back.data_to_read.data = rest_uuid
        restaurant_chosen(c_back.data_to_read)
    else:
        if callback_data != customermenus.cart_button.callback_data:
            new_c_back = DBInterface(call)
            dishes_uuids = c_back.get_from_cart("dishes_uuids")
            if not dishes_uuids:
                dishes_uuids = []
            dishes_uuids.append(callback_data)
            new_c_back.data_to_read.data = dishes_uuids
            new_c_back.add_to_cart("dishes_uuids")
            prices_calc(new_c_back.data_to_read)
        pay_button = types.InlineKeyboardButton(text=customermenus.PAY_BTN, callback_data=customermenus.PAY_BTN)
        add_more_button = types.InlineKeyboardButton(text=customermenus.ADD_MORE_BTN,
                                                     callback_data=customermenus.ADD_MORE_BTN)
        delete_item_button = types.InlineKeyboardButton(text=customermenus.DELETE_ITEM_BTN,
                                                        callback_data=customermenus.DELETE_ITEM_BTN)
        menu = types.InlineKeyboardMarkup(row_width=1)
        menu.add(pay_button, add_more_button, delete_item_button, customermenus.cancel_order_button)
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
        new_text = "\n".join([customermenus.YOUR_CART_MSG,
                              f"{dishes_displayed}",
                              "----",
                              customermenus.SUBTOTAL_MSG,
                              f"{customermenus.CURRENCY}{subtotal}",
                              customermenus.COURIER_FEE_MSG,
                              f"{customermenus.CURRENCY}{courier_fee}",
                              customermenus.SERVICE_FEE_MSG,
                              f"{customermenus.CURRENCY}{service_fee}",
                              "----",
                              customermenus.TOTAL_MSG,
                              f"{customermenus.CURRENCY}{total}"])
        bot.edit_message_text(new_text, customer_id, message_id, reply_markup=menu)


@bot.callback_query_handler(func=lambda call: customermenus.YOUR_CART_MSG in call.message.text)
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
    customer_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    if c_back.data_to_read.data == customermenus.cancel_order_button.callback_data:
        clear_cart(c_back.data_to_read)
    elif c_back.data_to_read.data == customermenus.DELETE_ITEM_BTN:
        deletion_menu = types.InlineKeyboardMarkup(row_width=1)
        dishes_uuids = c_back.get_from_cart("dishes_uuids")
        dishes = {}
        if dishes_uuids:
            for dish_uuid in dishes_uuids:
                c_back.data_to_read.data = dish_uuid
                dish_name = c_back.get_dish()[0]
                dishes[dish_uuid] = dish_name
            for dish_uuid in dishes_uuids:
                deletion_menu.add(types.InlineKeyboardButton(text=dishes[dish_uuid], callback_data=dish_uuid))
        deletion_menu.add(customermenus.cart_button)
        bot.edit_message_text(customermenus.DELETE_ITEM_MSG, customer_id, message_id, reply_markup=deletion_menu)
    elif c_back.data_to_read.data == customermenus.ADD_MORE_BTN:
        c_back.data_to_read.data = c_back.get_from_cart("restaurant_uuid")
        c_back.data_to_read.message.text = customermenus.ADD_MORE_BTN
        restaurant_chosen(c_back.data_to_read)
    elif c_back.data_to_read.data == customermenus.PAY_BTN:
        bot.send_message(customer_id, customermenus.IN_DEV)
        clear_cart(c_back.data_to_read)


@bot.callback_query_handler()
@logger_decorator_callback
def item_deletion(call: types.CallbackQuery) -> None:
    """Delete selected item from Customer's cart.
    Call cart menu.

    Args:
        call: Callback query with Customer's input from item deletion menu.

    """
    c_back = DBInterface(call)
    if c_back.data_to_read.data != customermenus.cart_button.callback_data:
        dishes_uuids = c_back.get_from_cart("dishes_uuids")
        if dishes_uuids:
            dishes_uuids.remove(c_back.data_to_read.data)
            c_back.data_to_read.data = dishes_uuids
            c_back.add_to_cart("dishes_uuids")
        prices_calc(c_back.data_to_read)
    c_back.data_to_read.data = customermenus.cart_button.callback_data
    is_dish_added(c_back.data_to_read)


# Payment block. # TODO
@bot.callback_query_handler()
@logger_decorator_callback
def payment_confirmation(call: types.CallbackQuery) -> None:
    """"""
    pass




def main():
    logger.info("The bot is running.")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
