import telebot as tb
import telebot.types as types
from environs import Env

import customermenus
from customer_bot.langs.customer_bot_textes_en_US import PAY_BTN
from loggertool import logger, logger_decorator_callback, logger_decorator_msg
from customerdbtools import DBInterface as Interface

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
    msg = Interface(message)
    if msg.user_in_db():
        bot.send_message(message.from_user.id, customermenus.MAIN_MENU_MSG, reply_markup=customermenus.main_menu)
    else:
        start(message)


@logger_decorator_msg
def phone_from_msg(message: types.Message) -> str | None:
    """Check if manually entered phone number is valid and add it into the DB.Customers if so.

    Args:
        message: Manually entered phone number.

    Returns:
        Phone number if valid, None otherwise.

    """
    phone_number = str(message.text)
    for symbol in phone_number:
        if not symbol.isdigit():
            phone_number = phone_number.replace(symbol, "")
    if len(phone_number) not in range(2, customermenus.MAX_PHONE_LENGTH_WO_PREFIX + 1):
        return None
    else:
        phone_number = f"{customermenus.PHONE_NUM_PREFIX}" + phone_number
        msg = Interface(message)
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
    c_back = Interface(call)
    bot.answer_callback_query(c_back.input_object.id, customermenus.DELETING_CART_ALERT, show_alert=True)
    bot.delete_message(c_back.input_object.from_user.id, c_back.input_object.message.message_id)
    c_back.delete_cart()
    show_main_menu(callback_to_msg(c_back.input_object))


# Sing in/sign up block.
@bot.message_handler(commands=["start"])
@logger_decorator_msg
def start(message: types.Message) -> None:
    """Commence interaction between Customer and the bot. Check if Customer in the DB and
    start corresponding interaction sequence.

    Args:
        message: /start command from Customer.

    """
    msg = Interface(message)
    msg.delete_cart()
    user = msg.user_in_db()
    if user:
        bot.send_message(message.from_user.id, customermenus.WELCOME_BACK_MSG + user)
        show_main_menu(message)
    else:
        bot.send_message(message.from_user.id, customermenus.FIRST_WELCOME_MSG)
        bot.send_message(
            message.from_user.id,
            customermenus.ASK_AGREEMENT_MSG,
            reply_markup=customermenus.agreement_menu
        )


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
    """Commence Customer sign up sequence. Add new Customer to the DB.

    Args:
        message: Accept Agreement input from Customer.

    """
    msg = Interface(message)
    user = msg.user_in_db()
    if not user:
        msg.add_customer()
    bot.send_message(message.from_user.id, customermenus.AGREEMENT_ACCEPTED_MSG)
    bot.send_message(
        message.from_user.id,
        customermenus.REG_NAME_MSG,
        reply_markup=types.ForceReply(input_field_placeholder=customermenus.REG_NAME_PLACEHOLDER)
    )


@bot.message_handler(
    func=lambda message: message.reply_to_message and \
                         message.reply_to_message.text == customermenus.REG_NAME_MSG
)
@logger_decorator_msg
def reg_name(message: types.Message) -> None:
    """Add Customer's name to the DB. Ask Customer to choose phone number input method.

    Args:
        message: Customer's name.

    """
    msg = Interface(message)
    msg.update_name()
    bot.send_message(message.from_user.id, customermenus.REG_NAME_RECEIVED_MSG + message.text)
    bot.send_message(
        message.from_user.id,
        customermenus.REG_PHONE_METHOD_MSG,
        reply_markup=customermenus.reg_phone_menu
    )


@bot.message_handler(content_types=["contact"])
@bot.message_handler(regexp=customermenus.REG_PHONE_METHOD_MSG)
@logger_decorator_msg
def contact(message: types.Message) -> None:
    """Add Customer's phone number imported via Telegram contact info into the DB.
    Ask Customer to choose delivery address input method.

    Args:
        message: Customer's Telegram contact info.

    """
    phone_number = message.contact.phone_number
    msg = Interface(message)
    msg.update_phone_number(phone_number)
    bot.send_message(message.from_user.id, customermenus.PHONE_RECEIVED_MSG + phone_number)
    bot.send_message(
        message.from_user.id,
        customermenus.REG_LOCATION_MSG,
        reply_markup=customermenus.reg_location_menu
    )


@bot.message_handler(regexp=customermenus.REG_PHONE_MAN_BTN)
@logger_decorator_msg
def reg_phone_str(message: types.Message) -> None:
    """Ask Customer to input phone number manually.

    Args:
        message: Request form Customer to input phone number manually.

    """
    bot.send_message(
        message.from_user.id,
        customermenus.REG_PHONE_MSG,
        reply_markup=types.ForceReply(input_field_placeholder=customermenus.REG_PHONE_PLACEHOLDER)
    )


@bot.message_handler(
    func=lambda message: message.reply_to_message and \
                         message.reply_to_message.text == customermenus.REG_PHONE_MSG
)
@logger_decorator_msg
def reg_phone(message: types.Message) -> None:
    """Check if phone number was added to the DB. Ask Customer to choose delivery input method if so.
    Ask Customer to input phone number again otherwise.

    Args:
        message: Customer's phone number entered manually.

    """
    phone_number = phone_from_msg(message)
    if not phone_number:
        bot.send_message(message.from_user.id, customermenus.INVALID_PHONE_MSG)
        bot.send_message(
            message.from_user.id,
            customermenus.REG_PHONE_MSG,
            reply_markup=types.ForceReply(input_field_placeholder=customermenus.REG_PHONE_PLACEHOLDER)
        )
    else:
        bot.send_message(message.from_user.id, customermenus.PHONE_RECEIVED_MSG + phone_number)
        bot.send_message(
            message.from_user.id,
            customermenus.REG_LOCATION_MSG,
            reply_markup=customermenus.reg_location_menu
        )


@bot.message_handler(content_types=["location"])
@bot.message_handler(regexp=customermenus.REG_LOCATION_BTN)
@logger_decorator_msg
def reg_location(message: types.Message) -> None:
    """Add location to the DB. Proceed to main menu.

    Args:
        message: Location from Customer.

    """
    msg = Interface(message)
    msg.update_customer_location()
    bot.send_message(message.from_user.id, customermenus.REG_LOCATION_RECEIVED_MSG)
    latitude = msg.input_object.location.latitude
    longitude = msg.input_object.location.longitude
    bot.send_location(message.from_user.id, latitude, longitude)
    show_main_menu(message)


# Main menu block.
@bot.message_handler(regexp=customermenus.OPTIONS_BTN)
@logger_decorator_msg
def options(message: types.Message) -> None:
    """Show options menu.

    Args:
        message: Options request from Customer.

    """
    bot.send_message(message.from_user.id, customermenus.OPTIONS_MSG, reply_markup=customermenus.options_menu)


@bot.message_handler(regexp=customermenus.MY_ORDERS_BTN)
@logger_decorator_msg
def my_orders(message: types.Message) -> None:
    """Send Customer their order history.

    Args:
        message: Message from Customer with corresponding request.

    """
    msg = Interface(message)
    orders = msg.show_my_orders()
    if not orders:
        bot.send_message(message.from_user.id, customermenus.NO_ORDERS_FOUND_MSG)
        show_main_menu(message)
    else:
        while orders:
            bot.send_message(message.from_user.id, customermenus.my_orders_msg(orders))
        show_main_menu(message)


@bot.message_handler(regexp=customermenus.NEW_ORDER_BTN)
@logger_decorator_msg
def new_order(message: types.Message) -> None:
    """Commence order creation sequence. Check if User location is provided. If location is provided, ask confirmation.

    Args:
        message: Request form Customer to create new order.

    """
    msg = Interface(message)
    location = msg.check_if_location()
    if not location:
        bot.send_message(message.from_user.id, customermenus.LOCATION_NOT_FOUND_MSG)
        show_main_menu(message)
    else:
        bot.send_message(
            message.from_user.id,
            customermenus.CONFIRM_LOCATION_MSG,
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.send_location(
            message.from_user.id,
            location["lat"],
            location["lon"],
            reply_markup=customermenus.confirm_location_menu
        )


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
    bot.send_message(
        message.from_user.id,
        customermenus.RESET_CONTACT_INFO_MSG,
        reply_markup=customermenus.reset_info_menu
    )


@bot.message_handler(regexp=customermenus.DELETE_PROFILE_BTN)
@logger_decorator_msg
def delete_profile(message: types.Message) -> None:
    """Ask Customer for profile deletion confirmation.

    Args:
        message: Deletion request from Customer.

    """
    bot.send_message(
        message.from_user.id,
        customermenus.DELETE_PROFILE_MSG,
        reply_markup=customermenus.confirm_delete_profile_menu
    )


# Contact Info reset block.
@bot.message_handler(regexp=customermenus.CONFIRM_RESET_BTN)
@logger_decorator_msg
def confirm_reset(message: types.Message) -> None:
    """Commence contact info reset sequence.

    Args:
        message: Confirmation from Customer.

    """
    msg = Interface(message)
    msg.delete_customer()
    bot.send_message(message.from_user.id, customermenus.CONTACT_INFO_DELETED_MSG)
    agreement_accepted(message)


# Profile deletion block.
@bot.message_handler(regexp=customermenus.CONFIRM_DELETE_PROFILE_BTN)
@logger_decorator_msg
def confirm_delete(message: types.Message) -> None:
    """Delete Customer's profile from DB.

    Args:
        message: Confirmation from Customer.

    """
    msg = Interface(message)
    msg.delete_customer()
    bot.send_message(message.from_user.id, customermenus.PROFILE_DELETED_MSG, reply_markup=types.ReplyKeyboardRemove())


# Creating order sequence block.
@bot.callback_query_handler(func=lambda call: call.message.location)
@logger_decorator_callback
def check_location_confirmation(call: types.CallbackQuery) -> None:
    """Process Customer's response to location confirmation request. Show Customer restaurant type selection menu if
    confirmed, send back to main menu if not.

    Args:
        call: Callback query from Customer with response to location confirmation request.

    """
    c_back = Interface(call)
    bot.delete_message(c_back.input_object.from_user.id, c_back.input_object.message.id - 1)
    bot.delete_message(c_back.input_object.from_user.id, c_back.input_object.message.id)
    if c_back.input_object.data == customermenus.WRONG_LOCATION_MSG:
        bot.send_message(c_back.input_object.from_user.id, customermenus.REQUEST_NEW_LOCATION_MSG)
        show_main_menu(callback_to_msg(call))
    elif call.data == customermenus.CONFIRM_LOCATION_BTN:
        c_back.new_cart()
        restaurant_types = Interface.show_restaurant_types()
        menu = types.InlineKeyboardMarkup(row_width=1)
        if restaurant_types:
            for restaurant_type in restaurant_types:
                menu.add(types.InlineKeyboardButton(text=restaurant_type[0], callback_data=restaurant_type[0]))
        menu.add(customermenus.back_button)
        bot.send_message(
            call.from_user.id,
            customermenus.CHOOSE_REST_TYPE_MSG,
            reply_markup=menu
        )


@bot.callback_query_handler(func=lambda call: call.message.text == customermenus.CHOOSE_REST_TYPE_MSG)
@logger_decorator_callback
def rest_type_chosen(call: types.CallbackQuery) -> None:
    """Process Customer's response to restaurant type selection. Show Customer restaurants of selected type and add
    restaurant type to the Customer's cart or go back to main menu if "go back" button is clicked.
    
    Args:
        call: Callback query from Customer with response to restaurant type selection.

    """
    c_back = Interface(call)
    if c_back.input_object.data == customermenus.back_button.callback_data:
        bot.answer_callback_query(c_back.input_object.id, customermenus.EXITING_ORDER_MENU_MSG)
        bot.delete_message(c_back.input_object.from_user.id, c_back.input_object.message.message_id)
        c_back.delete_cart()
        msg = callback_to_msg(c_back.input_object)
        show_main_menu(msg)
    else:
        c_back.add_to_cart("restaurant_type")
        restaurants = c_back.show_restaurants()
        menu = types.InlineKeyboardMarkup(row_width=1)
        if restaurants:
            for restaurant in restaurants:
                menu.add(types.InlineKeyboardButton(text=restaurant[0], callback_data=restaurant[1]))
        menu.add(customermenus.back_button)
        bot.edit_message_text(
            customermenus.SELECTED_REST_TYPE_MSG + f"\n{call.data}\n" + customermenus.CHOOSE_REST_MSG,  # TODO export to texts as lambda
            call.from_user.id,
            call.message.message_id,
            reply_markup=menu
        )


@bot.callback_query_handler(func=lambda call: customermenus.CHOOSE_REST_MSG in call.message.text)
@logger_decorator_callback
def restaurant_chosen(call: types.CallbackQuery) -> None:
    """Process Customer's response to restaurant selection. Show Customer dish types available in selected restaurant
    and add restaurant UUID to the Customer's cart or go back to main menu if "go back" button is clicked.

    Args:
        call: Callback query from Customer with response to restaurant selection.

    """
    c_back = Interface(call)
    if c_back.input_object.data == customermenus.back_button.callback_data:
        bot.answer_callback_query(c_back.input_object.id, customermenus.DELETING_CART_ALERT, show_alert=True)
        bot.delete_message(c_back.input_object.from_user.id, c_back.input_object.message.message_id)
        c_back.delete_cart()
        show_main_menu(callback_to_msg(call))
    else:
        c_back.add_to_cart("restaurant_uuid")
        dish_categories = c_back.show_dish_categories()
        menu = types.InlineKeyboardMarkup(row_width=1)
        if dish_categories:
            for category in dish_categories:
                menu.add(types.InlineKeyboardButton(text=category[0], callback_data=category[0]))
        menu.add(customermenus.cart_button)
        menu.add(customermenus.back_button)
        menu.add(customermenus.cancel_order_button)
        c_back = Interface(call)
        restaurant = c_back.rest_name_by_uuid()
        bot.edit_message_text(
            customermenus.SELECTED_REST_MSG + f"\n{restaurant}\n" + customermenus.CHOOSE_DISH_CATEGORY_MSG,  # TODO export to texts as lambda
            call.from_user.id,
            call.message.message_id,
            reply_markup=menu
        )


@bot.callback_query_handler(func=lambda call: customermenus.CHOOSE_DISH_CATEGORY_MSG in call.message.text)
@logger_decorator_callback
def dish_category_chosen(call: types.CallbackQuery) -> None:
    """Process Customer's response to dish category selection. Show Customer dishes of selected category
    available in selected restaurant or go back to restaurant selection menu if "go back" button is clicked.
    Show Customer their cart or clear it if corresponding buttons are clicked.

    Args:
        call: Callback query from Customer with response to dish category selection.

    """
    c_back = Interface(call)
    if c_back.input_object.data == customermenus.back_button.callback_data:
        c_back.delete_from_cart("restaurant_uuid")
        c_back.input_object.data = c_back.get_from_cart("restaurant_type")
        rest_type_chosen(c_back.input_object)
    elif c_back.input_object.data == customermenus.cancel_order_button.callback_data:
        clear_cart(c_back.input_object)
    elif c_back.input_object.data == customermenus.cart_button.callback_data:
        is_dish_added(c_back.input_object)
    else:
        dishes = c_back.show_dishes()
        menu = types.InlineKeyboardMarkup(row_width=1)
        if dishes:
            for dish in dishes:
                menu.add(types.InlineKeyboardButton(text=dish[0], callback_data=dish[1]))
        menu.add(customermenus.cart_button)
        menu.add(customermenus.back_button)
        menu.add(customermenus.cancel_order_button)
        bot.edit_message_text(
            customermenus.SELECTED_DISH_CAT_MSG + f"\n{c_back.input_object.data}\n" + customermenus.CHOOSE_DISH_MSG,  # TODO export to texts as lambda
            c_back.input_object.from_user.id,
            c_back.input_object.message.message_id,
            reply_markup=menu
        )


@bot.callback_query_handler(func=lambda call: customermenus.CHOOSE_DISH_MSG in call.message.text)
@logger_decorator_callback
def dish_chosen(call: types.CallbackQuery) -> None:
    """Process Customer's response to dish selection. Show Customer dish selection confirmation menu displaying
    dish description and price or go back to restaurant selection menu if "go back" button is clicked.
    Show Customer their cart or clear it if corresponding buttons are clicked.

    Args:
        call: Callback query from Customer with response to dish selection.

    """
    c_back = Interface(call)
    if c_back.input_object.data == customermenus.back_button.callback_data:
        data = c_back.get_from_cart("restaurant_uuid")
        c_back.input_object.data = data
        restaurant_chosen(c_back.input_object)
    elif c_back.input_object.data == customermenus.cancel_order_button.callback_data:
        clear_cart(c_back.input_object)
    elif c_back.input_object.data == customermenus.cart_button.callback_data:
        is_dish_added(c_back.input_object)
    else:
        add_dish_button = types.InlineKeyboardButton(text=customermenus.ADD_DISH_BTN,
                                                     callback_data=c_back.input_object.data)
        menu = types.InlineKeyboardMarkup(row_width=2)
        menu.add(customermenus.back_button, add_dish_button)
        dish = c_back.get_dish()
        new_text = "\n".join(  # TODO export to texts as lambda
            [
                customermenus.SELECTED_DISH_MSG,
                f"{dish[0]}",
                customermenus.DISH_DESC_MSG,
                f"{dish[1]}",
                customermenus.DISH_PRICE_MSG,
                f"{customermenus.CURRENCY}{dish[2]}"
            ]
        )
        bot.edit_message_text(
            new_text,
            c_back.input_object.from_user.id,
            c_back.input_object.message.message_id,
            reply_markup=menu
        )


@bot.callback_query_handler(func=lambda call: customermenus.SELECTED_DISH_MSG in call.message.text)
@logger_decorator_callback
def is_dish_added(call: types.CallbackQuery) -> None:
    """Process Customer's response to selected dish confirmation. Show Customer's cart menu displaying
    dishes and price or go back to dish category selection menu if confirmation isn't obtained.

    Args:
        call: Callback query from Customer with response to selected dish confirmation.

    """
    c_back = Interface(call)  # TODO
    if c_back.input_object.data == customermenus.back_button.callback_data:
        data = c_back.get_from_cart("restaurant_uuid")
        c_back.input_object.data = data
        restaurant_chosen(c_back.input_object)
    else:
        if c_back.input_object.data != customermenus.cart_button.callback_data:
            dishes_uuids = c_back.get_from_cart("dishes_uuids")  # TODO FIX BUG!!!
            if not dishes_uuids:
                dishes_uuids = []
            dishes_uuids.append(c_back.input_object.data)
            c_back.input_object.data = dishes_uuids
            c_back.add_to_cart("dishes_uuids")
            subtotal = 0
            for dish in dishes_uuids:
                c_back.input_object.data = dish
                dish_price = c_back.get_dish()[2]
                subtotal += dish_price
            c_back.input_object.data = subtotal
            c_back.add_to_cart("subtotal")
        pay_button = types.InlineKeyboardButton(text=customermenus.PAY_BTN, callback_data=customermenus.PAY_BTN)
        add_more_button = types.InlineKeyboardButton(text=customermenus.ADD_MORE_BTN, callback_data=customermenus.ADD_MORE_BTN)
        delete_item_button = types.InlineKeyboardButton(
            text=customermenus.DELETE_ITEM_BTN,
            callback_data=customermenus.DELETE_ITEM_BTN
        )
        menu = types.InlineKeyboardMarkup(row_width=1)
        menu.add(pay_button, add_more_button, delete_item_button, customermenus.cancel_order_button)
        c_back.input_object.data = c_back.get_from_cart("dishes_uuids")  # TODO: transfer to textes as lambda expr.
        dishes = []
        if c_back.input_object.data:
            for dish in c_back.input_object.data:
                c_back.input_object.data = dish
                dish_name = c_back.get_dish()[0]
                dishes.append(dish_name)
        subtotal = c_back.get_from_cart("subtotal")
        new_text = "\n".join(
            [
                customermenus.YOUR_CART_MSG,
                f"{dishes}",
                customermenus.SUBTOTAL_MSG,
                f"{customermenus.CURRENCY}{subtotal}"
            ]
        )
        bot.edit_message_text(
            new_text,
            c_back.input_object.from_user.id,
            c_back.input_object.message.message_id,
            reply_markup=menu
        )


@bot.callback_query_handler()
@logger_decorator_callback
def cart_actions(call: types.CallbackQuery) -> None:
    """"""
    c_back = Interface(call)

    pass


# TODO: add payment block.


def main():
    logger.info("The bot is running.")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
