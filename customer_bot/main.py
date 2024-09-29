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
    """Show Customer main menu.

    Args:
        message: Main menu request from Customer.

    """
    bot.send_message(message.from_user.id, customermessages.MAIN_MENU_MSG, reply_markup=customermenus.main_menu)


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


# Sing in/sign up block.
@bot.message_handler(commands=["start"])
def start(message: types.Message) -> None:
    """Commence interaction between Customer and the bot. Check if Customer in the DB and
    start corresponding interaction sequence.

    Args:
        message: /start command from Customer.

    """
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
    phone_number = "+" + message.contact.phone_number
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
    pass


@bot.message_handler(regexp=customermenus.NEW_ORDER_BTN)
def new_order(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """
    pass


@bot.message_handler(regexp=customermenus.RESET_CONTACT_INFO_BTN)
def reset_contact_info(message: types.Message) -> None:
    """Ask Customer for contact info confirmation.

    Args:
        message: Request form Customer to reset contact info.

    """
    bot.send_message(
        message.from_user.id,
        customermessages.RESET_CONTACT_INFO_MSG,
        reply_markup=customermenus.reset_info_menu
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


def main():
    logger.info("The bot is running.")
    bot.infinity_polling()


if __name__ == "__main__":
    main()