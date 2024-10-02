import telebot as tb
import telebot.types as types
from environs import Env

import customermenus
import customermessages
from loggertool import logger
from customerdbtools import DBInterface as Interface

env = Env()
env.read_env()

BOT_TOKEN = env.str("CUSTOMER_BOT_TOKEN")

bot = tb.TeleBot(token=BOT_TOKEN)


# Auxiliary functions.
def show_main_menu(message: types.Message) -> None:
    """Show Customer main menu if Customer is in the DB, otherwise call start().

    Args:
        message: Main menu request from Customer.

    """
    if Interface.user_in_db(message):
        bot.send_message(message.from_user.id, customermessages.MAIN_MENU_MSG, reply_markup=customermenus.main_menu)
    else:
        start(message)


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
    if len(phone_number) not in range(2, 12):
        return None
    else:
        phone_number = "+49" + phone_number
        Interface.update_phone_number(message.from_user.id, phone_number)
        return phone_number


def callback_to_msg(call: types.CallbackQuery) -> types.Message:
    """

    Args:
        call:

    Returns:

    """
    call.message.from_user.id = call.from_user.id
    msg = call.message
    return msg


def clear_cart(call: types.CallbackQuery) -> None:
    """"""
    bot.answer_callback_query(call.id, customermessages.DELETING_CART_ALERT, show_alert=True)
    bot.delete_message(call.from_user.id, call.message.message_id)
    Interface.delete_cart(call.from_user.id)
    show_main_menu(callback_to_msg(call))


# Sing in/sign up block.
@bot.message_handler(commands=["start"])
def start(message: types.Message) -> None:
    """Commence interaction between Customer and the bot. Check if Customer in the DB and
    start corresponding interaction sequence.

    Args:
        message: /start command from Customer.

    """
    Interface.delete_cart(message.from_user.id)
    user = Interface.user_in_db(message)
    if user:
        bot.send_message(message.from_user.id, customermessages.WELCOME_BACK_MSG + user)
        show_main_menu(message)
    else:
        bot.send_message(message.from_user.id, customermessages.FIRST_WELCOME_MSG)
        bot.send_message(
            message.from_user.id,
            customermessages.ASK_AGREEMENT_MSG,
            reply_markup=customermenus.agreement_menu
        )


@bot.message_handler(regexp=customermenus.SHOW_AGREEMENT_BTN)
def show_agreement(message: types.Message) -> None:
    """Show Customer agreement.

    Args:
        message: Show Agreement input from Customer.

    """
    bot.send_message(message.from_user.id, customermessages.AGREEMENT_TEXT)


@bot.message_handler(regexp=customermenus.ACCEPT_AGREEMENT_BTN)
def agreement_accepted(message: types.Message) -> None:
    """Commence Customer sign up sequence. Add new Customer to the DB.

    Args:
        message: Accept Agreement input from Customer.

    """
    user = Interface.user_in_db(message)
    if not user:
        Interface.add_customer(message)
    bot.send_message(message.from_user.id, customermessages.AGREEMENT_ACCEPTED_MSG)
    bot.send_message(
        message.from_user.id,
        customermessages.REG_NAME_MSG,
        reply_markup=types.ForceReply(input_field_placeholder=customermessages.REG_NAME_PLACEHOLDER)
    )


@bot.message_handler(
    func=lambda message: message.reply_to_message and\
                         message.reply_to_message.text == customermessages.REG_NAME_MSG
)
def reg_name(message: types.Message) -> None:
    """Add Customer's name to the DB. Ask Customer to choose phone number input method.

    Args:
        message: Customer's name.

    """
    Interface.update_name(message)
    bot.send_message(message.from_user.id, customermessages.REG_NAME_RECEIVED_MSG + message.text)
    bot.send_message(
        message.from_user.id,
        customermessages.REG_PHONE_METHOD_MSG,
        reply_markup=customermenus.reg_phone_menu
    )


@bot.message_handler(content_types=["contact"])
@bot.message_handler(regexp=customermessages.REG_PHONE_METHOD_MSG)
def contact(message: types.Message) -> None:
    """Add Customer's phone number imported via Telegram contact info into the DB.
    Ask Customer to choose delivery address input method.

    Args:
        message: Customer's Telegram contact info.

    """
    phone_number = message.contact.phone_number
    Interface.update_phone_number(message.from_user.id, phone_number)
    bot.send_message(message.from_user.id, customermessages.PHONE_RECEIVED_MSG + phone_number)
    bot.send_message(
        message.from_user.id,
        customermessages.REG_LOCATION_MSG,
        reply_markup=customermenus.reg_location_menu
    )


@bot.message_handler(regexp=customermenus.REG_PHONE_MAN_BTN)
def reg_phone_str(message: types.Message) -> None:
    """Ask Customer to input phone number manually.

    Args:
        message: Request form Customer to input phone number manually.

    """
    bot.send_message(
        message.from_user.id,
        customermessages.REG_PHONE_MSG,
        reply_markup=types.ForceReply(input_field_placeholder=customermessages.REG_PHONE_PLACEHOLDER)
    )


@bot.message_handler(
    func=lambda message: message.reply_to_message and\
                         message.reply_to_message.text == customermessages.REG_PHONE_MSG
)
def reg_phone(message: types.Message) -> None:
    """Check if phone number was added to the DB. Ask Customer to choose delivery input method if so.
    Ask Customer to input phone number again otherwise.

    Args:
        message: Customer's phone number entered manually.

    """
    phone_number = phone_from_msg(message)
    if not phone_number:
        bot.send_message(message.from_user.id, customermessages.INVALID_PHONE_MSG)
        bot.send_message(
            message.from_user.id,
            customermessages.REG_PHONE_MSG,
            reply_markup=types.ForceReply(input_field_placeholder=customermessages.REG_PHONE_PLACEHOLDER)
        )
    else:
        bot.send_message(message.from_user.id, customermessages.PHONE_RECEIVED_MSG + phone_number)
        bot.send_message(
            message.from_user.id,
            customermessages.REG_LOCATION_MSG,
            reply_markup=customermenus.reg_location_menu
        )

@bot.message_handler(content_types=["location"])
@bot.message_handler(regexp=customermenus.REG_LOCATION_BTN)
def reg_location(message: types.Message) -> None:
    """Add location to the DB. Proceed to main menu.

    Args:
        message: Location from Customer.

    """
    latitude = message.location.latitude
    longitude = message.location.longitude
    Interface.update_customer_location(latitude, longitude, message)
    bot.send_message(message.from_user.id, customermessages.REG_LOCATION_RECEIVED_MSG)
    bot.send_location(message.from_user.id, latitude, longitude)
    show_main_menu(message)


# Main menu block.
@bot.message_handler(regexp=customermenus.OPTIONS_BTN)
def options(message: types.Message) -> None:
    """Show options menu.

    Args:
        message: Options request from Customer.

    """
    bot.send_message(message.from_user.id, customermessages.OPTIONS_MSG, reply_markup=customermenus.options_menu)


@bot.message_handler(regexp=customermenus.MY_ORDERS_BTN)
def my_orders(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """
    orders = Interface.show_my_orders(message)
    if not orders:
        bot.send_message(message.from_user.id, customermessages.NO_ORDERS_FOUND_MSG)
        show_main_menu(message)
    else:
        while orders:
            bot.send_message(message.from_user.id, customermessages.my_orders_msg(orders))
        show_main_menu(message)


@bot.message_handler(regexp=customermenus.NEW_ORDER_BTN)
def new_order(message: types.Message) -> None:
    """Commence order creation sequence. Check if User location is provided. If location is provided, ask confirmation.

    Args:
        message: Request form Customer to create new order.

    """
    location = Interface.check_if_location(message)
    if not location:
        bot.send_message(message.from_user.id, customermessages.LOCATION_NOT_FOUND_MSG)
        show_main_menu(message)
    else:
        bot.send_message(
            message.from_user.id,
            customermessages.CONFIRM_LOCATION_MSG,
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
def main_menu(message: types.Message) -> None:
    """Get back to main menu.

    Args:
        message: Main menu request from Customer.

    """
    show_main_menu(message)


# TODO Contact support.
@bot.message_handler(regexp=customermenus.CONTACT_SUPPORT_BTN)
def contact_support(message: types.Message) -> None:
    """

    Args:
        message:

    """
    pass


@bot.message_handler(regexp=customermenus.RESET_CONTACT_INFO_BTN)
def reset_contact_info(message: types.Message) -> None:
    """Ask Customer for contact info reset confirmation.

    Args:
        message: Request form Customer to reset contact info.

    """
    bot.send_message(
        message.from_user.id,
        customermessages.RESET_CONTACT_INFO_MSG,
        reply_markup=customermenus.reset_info_menu
    )


@bot.message_handler(regexp=customermenus.DELETE_PROFILE_BTN)
def delete_profile(message: types.Message) -> None:
    """Ask Customer for profile deletion confirmation.

    Args:
        message: Deletion request from Customer.

    """
    bot.send_message(
        message.from_user.id,
        customermessages.DELETE_PROFILE_MSG,
        reply_markup=customermenus.confirm_delete_profile_menu
    )


#Contact Info reset block.
@bot.message_handler(regexp=customermenus.CONFIRM_RESET_BTN)
def confirm_reset(message: types.Message) -> None:
    """Commence contact info reset sequence.

    Args:
        message: Confirmation from Customer.

    """
    Interface.delete_customer(message)
    bot.send_message(message.from_user.id, customermessages.CONTACT_INFO_DELETED_MSG)
    agreement_accepted(message)


#Profile deletion block.
@bot.message_handler(regexp=customermenus.CONFIRM_DELETE_PROFILE_BTN)
def confirm_delete(message: types.Message) -> None:
    """Delete Customer's profile from DB.

    Args:
        message: Confirmation from Customer.

    """
    Interface.delete_customer(message)
    bot.send_message(message.from_user.id, customermessages.PROFILE_DELETED_MSG)


# Creating order sequence block.
@bot.callback_query_handler(func=lambda call: call.message.location)
def check_location_confirmation(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """
    bot.delete_message(call.from_user.id, call.message.id - 1)
    bot.delete_message(call.from_user.id, call.message.id)
    if call.data == customermenus.WRONG_LOCATION_MSG:
        bot.send_message(call.from_user.id, customermessages.REQUEST_NEW_LOCATION_MSG)
        msg = callback_to_msg(call)
        show_main_menu(msg)
    elif call.data == customermenus.CONFIRM_LOCATION_BTN:
        Interface.new_cart(call)
        restaurant_types = Interface.show_restaurant_types()
        menu = types.InlineKeyboardMarkup(row_width=1)
        if restaurant_types:
            for restaurant_type in restaurant_types:
                menu.add(types.InlineKeyboardButton(text=restaurant_type[0], callback_data=restaurant_type[0]))
        menu.add(customermenus.back_button)
        bot.send_message(
            call.from_user.id,
            customermessages.CHOOSE_REST_TYPE_MSG,
            reply_markup=menu
        )

@bot.callback_query_handler(func=lambda call: call.message.text == customermessages.CHOOSE_REST_TYPE_MSG)
def rest_type_chosen(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """
    if call.data == customermenus.back_button.callback_data:
        bot.answer_callback_query(call.id, customermessages.EXITING_ORDER_MENU_MSG)
        bot.delete_message(call.from_user.id, call.message.message_id)
        Interface.delete_cart(call.from_user.id)
        msg = callback_to_msg(call)
        show_main_menu(msg)
    else:
        Interface.add_to_cart("restaurant_type", call)
        restaurants = Interface.show_restaurants(call.data)
        menu = types.InlineKeyboardMarkup(row_width=1)
        if restaurants:
            for restaurant in restaurants:
                menu.add(types.InlineKeyboardButton(text=restaurant[0], callback_data=restaurant[1]))
        menu.add(customermenus.back_button)
        bot.edit_message_text(
            customermessages.SELECTED_REST_TYPE_MSG + f"\n{call.data}\n" + customermessages.CHOOSE_REST_MSG,
            call.from_user.id,
            call.message.message_id,
            reply_markup=menu
        )


@bot.callback_query_handler(func=lambda call: customermessages.CHOOSE_REST_MSG in call.message.text)
def restaurant_chosen(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """
    if call.data == customermenus.back_button.callback_data:
        bot.answer_callback_query(call.id, customermessages.DELETING_CART_ALERT, show_alert=True)
        bot.delete_message(call.from_user.id, call.message.message_id)
        Interface.delete_cart(call.from_user.id)
        show_main_menu(callback_to_msg(call))
    else:
        Interface.add_to_cart("restaurant_uuid", call)
        dish_categories = Interface.show_dish_categories(call.data)
        menu = types.InlineKeyboardMarkup(row_width=1)
        if dish_categories:
            for category in dish_categories:
                menu.add(types.InlineKeyboardButton(text=category[0], callback_data=category[0]))
        menu.add(customermenus.cart_button)
        menu.add(customermenus.back_button)
        menu.add(customermenus.cancel_order_button)
        restaurant = Interface.rest_name_by_uuid(call.data)
        bot.edit_message_text(
            customermessages.SELECTED_REST_MSG + f"\n{restaurant}\n" + customermessages.CHOOSE_DISH_CATEGORY_MSG,
            call.from_user.id,
            call.message.message_id,
            reply_markup=menu
        )


@bot.callback_query_handler(func=lambda call: customermessages.CHOOSE_DISH_CATEGORY_MSG in call.message.text)
def dish_category_chosen(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """
    if call.data == customermenus.back_button.callback_data:
        Interface.delete_from_cart("restaurant_uuid", call)
        call.data = Interface.get_from_cart("restaurant_type", call)
        rest_type_chosen(call)
    elif call.data == customermenus.cancel_order_button.callback_data:
        clear_cart(call)
    elif call.data == customermenus.cart_button.callback_data:
        is_dish_added(call)
    else:
        dishes = Interface.show_dishes(call)
        menu = types.InlineKeyboardMarkup(row_width=1)
        if dishes:
            for dish in dishes:
                menu.add(types.InlineKeyboardButton(text=dish[0], callback_data=dish[1]))
        menu.add(customermenus.cart_button)
        menu.add(customermenus.back_button)
        menu.add(customermenus.cancel_order_button)
        bot.edit_message_text(
            customermessages.SELECTED_DISH_CAT_MSG + f"\n{call.data}\n" + customermessages.CHOOSE_DISH_MSG,
            call.from_user.id,
            call.message.message_id,
            reply_markup=menu
        )


@bot.callback_query_handler(func=lambda call: customermessages.CHOOSE_DISH_MSG in call.message.text)
def dish_chosen(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """
    if call.data == customermenus.back_button.callback_data:
        data = Interface.get_from_cart("restaurant_uuid", call)
        call.data = data
        restaurant_chosen(call)
    elif call.data == customermenus.cancel_order_button.callback_data:
        clear_cart(call)
    elif call.data == customermenus.cart_button.callback_data:
        is_dish_added(call)
    else:
        add_dish_button = types.InlineKeyboardButton(text=customermenus.ADD_DISH_BTN, callback_data=call.data)
        menu = types.InlineKeyboardMarkup(row_width=2)
        menu.add(customermenus.back_button, add_dish_button)
        dish = Interface.get_dish(call)
        new_text = "\n".join(
            [
                customermessages.SELECTED_DISH_MSG,
                f"{dish[0]}",
                customermessages.DISH_DESC_MSG,
                f"{dish[1]}",
                customermessages.DISH_PRICE_MSG,
                f"{customermessages.CURRENCY}{dish[2]}"
            ]
        )
        bot.edit_message_text(
            new_text,
            call.from_user.id,
            call.message.message_id,
            reply_markup=menu
        )


@bot.callback_query_handler(func=lambda call: customermessages.SELECTED_DISH_MSG in call.message.text)
def is_dish_added(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """
    if call.data == customermenus.back_button.callback_data:
        data = Interface.get_from_cart("restaurant_uuid", call)
        call.data = data
        restaurant_chosen(call)
    else:
        if call.data != customermenus.cart_button.callback_data:
            dishes_uuids = Interface.get_from_cart("dishes_uuids", call)  #TODO FIX BUG!!!
            if not dishes_uuids:
                dishes_uuids = []
            dishes_uuids.append(call.data)
            call.data = dishes_uuids
            Interface.add_to_cart("dishes_uuids", call)
            subtotal = 0
            for dish in dishes_uuids:
                call.data = dish
                dish_price = Interface.get_dish(call)[2]
                subtotal += dish_price
            call.data = subtotal
            Interface.add_to_cart("subtotal", call)
        pay_button = types.InlineKeyboardButton(text=customermenus.PAY_BTN, callback_data="DEV")
        add_more_button = types.InlineKeyboardButton(text=customermenus.ADD_MORE_BTN, callback_data="aaa")
        delete_item_button = types.InlineKeyboardButton(
            text=customermenus.DELETE_ITEM_BTN,
            callback_data=customermenus.DELETE_ITEM_BTN
        )
        menu = types.InlineKeyboardMarkup(row_width=1)
        menu.add(pay_button, add_more_button, delete_item_button, customermenus.cancel_order_button)
        call.data = Interface.get_from_cart("dishes_uuids", call)
        dishes = []
        if call.data:
            for dish in call.data:
                call.data = dish
                dish_name = Interface.get_dish(call)[0]
                dishes.append(dish_name)
        subtotal = Interface.get_from_cart("subtotal", call)
        new_text = "\n".join(
            [
                customermessages.YOUR_CART_MSG,
                f"{dishes}",
                customermessages.SUBTOTAL_MSG,
                f"{customermessages.CURRENCY}{subtotal}"
            ]
        )
        bot.edit_message_text(
            new_text,
            call.from_user.id,
            call.message.message_id,
            reply_markup=menu
        )



@bot.callback_query_handler()
def cart_actions(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """
    pass


def main():
    logger.info("The bot is running.")
    bot.infinity_polling()


if __name__ == "__main__":
    main()