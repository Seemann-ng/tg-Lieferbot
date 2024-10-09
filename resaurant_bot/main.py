import telebot as tb
import telebot.types as types
from environs import Env
from telebot.types import ForceReply

import restaurant_menus
from logger_tool import logger, logger_decorator_msg, logger_decorator_callback
from restaurant_db_tools import Interface as DBInterface
from restaurant_translations import texts

env = Env()
env.read_env()

BOT_TOKEN = env.str("RESTAURANT_BOT_TOKEN")

bot = tb.TeleBot(token=BOT_TOKEN)


@bot.message_handler(commands=["start"])
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
        bot.send_message(user_id, texts[lang_code]["ASK_REGISTRATION_MSG"], reply_markup=ForceReply())
    else:
        bot.send_message(user_id, texts[lang_code]["WELCOME_MSG"])


@bot.message_handler(func=lambda message: message.reply_to_message\
                                          and message.reply_to_message.text\
                                          in [lang["ASK_REGISTRATION_MSG"] for lang in texts.values()])
@logger_decorator_msg
def ask_registration(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """ # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    user_name = msg.data_to_read.from_user.username
    admin_id = msg.get_support_id()
    bot.send_message(admin_id, texts[lang_code]["REG_REQUEST_MSG"](user_name, user_id, message.text))
    bot.send_message(user_id, texts[lang_code]["REG_REQUEST_SENT_MSG"])


@bot.message_handler(commands=["add_dish"])
@logger_decorator_msg
def add_dish_command(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    dish_name = msg.data_to_read.text.split(maxsplit=1)[1]
    msg.add_dish(dish_name)
    bot.send_message(msg.user_id, texts[lang_code]["DISH_ADDED_MSG"](dish_name))


@bot.message_handler(commands=["edit_dish"])
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
    bot.send_message(user_id,
                     texts[lang_code]["EDIT_DISH_MSG"],
                     reply_markup=restaurant_menus.edit_dish_menu(lang_code, msg))


@bot.callback_query_handler(func=lambda call: call.message.text in [lang["EDIT_DISH_MSG"] for lang in texts.values()])
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
        bot.delete_message(user_id, message_id)
    else:
        bot.edit_message_text(texts[lang_code]["EDIT_DISH_CHOSEN_MSG"](c_back.get_dish_name()), user_id, message_id)
        bot.send_message(user_id,
                         texts[lang_code]["EDIT_DISH_PARAM_MSG"],
                         reply_markup=restaurant_menus.edit_dish_param_menu(lang_code, c_back))


# @bot.callback_query_handler(func=lambda call: call.message.text\
#                                               in [lang["EDIT_DISH_PARAM_MSG"] for lang in texts.values()])
# @logger_decorator_callback
# def req_new_dish_param(call: types.CallbackQuery) -> None: # TODO
#     """
#
#     Args:
#         call:
#
#     Returns:
#
#     """
#     c_back = DBInterface(call)
#     lang_code = c_back.get_rest_lang()
#     user_id = c_back.user_id
#     message_id = c_back.data_to_read.message.id
#     bot.delete_message(user_id, message_id - 1)
#     request = c_back.data_to_read.data.split(maxsplit=1)
#     param_to_edit = request[0]
#     dish_uuid = request[1]
#     if c_back.data_to_read.data == restaurant_menus.back_button(lang_code):
#         bot.delete_message(user_id, message_id)
#     elif param_to_edit == "cat":
#         bot.send_message(user_id, texts[lang_code][])


def main():
    logger.info("The bot is running.")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
