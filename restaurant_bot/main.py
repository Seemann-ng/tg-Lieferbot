import telebot as tb
import telebot.types as types
from environs import Env
from telebot.types import ForceReply

import restaurant_menus
from tools.logger_tool import logger, logger_decorator_msg, logger_decorator_callback
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

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    user_name = msg.data_to_read.from_user.username
    admin_id = msg.get_support_id()
    bot.send_message(admin_id, texts[lang_code]["REG_REQUEST_MSG"](user_name, user_id, message.text))
    bot.send_message(user_id, texts[lang_code]["REG_REQUEST_SENT_MSG"])


@bot.message_handler(commands=["select_language"])
@logger_decorator_msg
def change_lang_menu(message: types.Message) -> None:
    """Open language select menu.

    Args:
        message: Command with language select request.

    """
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    customer_id = msg.data_to_read.from_user.id
    bot.send_message(customer_id, texts[lang_code]["LANG_SEL_MENU"])
    bot.send_message(customer_id,
                     texts[lang_code]["CHANGE_LANG_MSG"],
                     reply_markup=restaurant_menus.lang_sel_menu(lang_code))


@bot.callback_query_handler(func= lambda call: call.message.text\
                                               in [lang["CHANGE_LANG_MSG"] for lang in texts.values()])
@logger_decorator_callback
def lang_set(call: types.CallbackQuery) -> None:
    """Change bot interface language.

    Args:
        call: Callback query with selected language info.

    """
    c_back = DBInterface(call)
    user_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    c_back.set_restaurant_lang()
    bot.delete_message(user_id, message_id - 1)
    bot.delete_message(user_id, message_id)
    bot.send_message(user_id, texts[c_back.data_to_read.data]["LANG_SELECTED_MSG"])


@bot.message_handler(commands=["open_shift"])
@logger_decorator_msg
def open_shift_command(message: types.Message) -> None:
    """
    
    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    msg.open_shift()
    bot.send_message(user_id, texts[lang_code]["OPEN_SHIFT_MSG"])


@bot.message_handler(commands=["close_shift"])
@logger_decorator_msg
def close_shift_command(message: types.Message) -> None:
    """
    
    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    msg.close_shift()
    bot.send_message(user_id, texts[lang_code]["CLOSE_SHIFT_MSG"])


@bot.message_handler(commands=["dish_available"])
@logger_decorator_msg
def dish_available_command(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    bot.send_message(user_id,
                     texts[lang_code]["DISH_AVAILABLE_SELECT_MSG"],
                     reply_markup=restaurant_menus.edit_dish_menu(lang_code, msg))


@bot.callback_query_handler(func=lambda call: call.message.text\
                                              in [lang["DISH_AVAILABLE_SELECT_MSG"] for lang in texts.values()])
@logger_decorator_callback
def dish_available_select(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    lang_code = c_back.get_rest_lang()
    user_id = c_back.user_id
    message_id = c_back.data_to_read.message.id
    c_back.set_dish_available()
    bot.delete_message(user_id, message_id)
    bot.send_message(user_id,
                     texts[lang_code]["DISH_SET_AVAILABLE_MSG"])


@bot.message_handler(commands=["dish_unavailable"])
@logger_decorator_msg
def dish_unavailable_command(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    bot.send_message(user_id,
                     texts[lang_code]["DISH_UNAVAILABLE_SELECT_MSG"],
                     reply_markup=restaurant_menus.edit_dish_menu(lang_code, msg))


@bot.callback_query_handler(func=lambda call: call.message.text\
                                              in [lang["DISH_UNAVAILABLE_SELECT_MSG"] for lang in texts.values()])
@logger_decorator_callback
def dish_unavailable_select(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    lang_code = c_back.get_rest_lang()
    user_id = c_back.user_id
    message_id = c_back.data_to_read.message.id
    bot.delete_message(user_id, message_id)
    c_back.set_dish_unavailable()
    bot.send_message(user_id,
                     texts[lang_code]["DISH_SET_UNAVAILABLE_MSG"])


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
    if dish_name := msg.data_to_read.text.split(maxsplit=1)[1]:
        msg.add_dish(dish_name)
        bot.send_message(msg.user_id, texts[lang_code]["DISH_ADDED_MSG"](dish_name))
    else:
        bot.send_message(msg.user_id, "No dish name found")


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


@bot.callback_query_handler(func=lambda call: call.message.text\
                                              in [lang["EDIT_DISH_PARAM_MSG"] for lang in texts.values()])
@logger_decorator_callback
def req_new_dish_param(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    lang_code = c_back.get_rest_lang()
    user_id = c_back.user_id
    message_id = c_back.data_to_read.message.id
    bot.delete_message(user_id, message_id - 1)
    bot.delete_message(user_id, message_id)
    request = c_back.data_to_read.data.split(maxsplit=1)
    param_to_edit = request[0]
    dish_uuid = request[1]
    if c_back.data_to_read.data == restaurant_menus.back_button(lang_code):
        bot.delete_message(user_id, message_id)
    elif param_to_edit == "cat":
        bot.send_message(user_id, texts[lang_code]["EDIT_CATEGORY_MSG"](dish_uuid), reply_markup=ForceReply())
    elif param_to_edit == "des":
        bot.send_message(user_id, texts[lang_code]["EDIT_DESCRIPTION_MSG"](dish_uuid), reply_markup=ForceReply())
    elif param_to_edit == "prc":
        bot.send_message(user_id, texts[lang_code]["EDIT_PRICE_MSG"](dish_uuid), reply_markup=ForceReply())


@bot.message_handler(func=lambda message: message.reply_to_message\
                                          and message.reply_to_message.text\
                                          in [lang["EDIT_CATEGORY_MSG"](message.reply_to_message.text.split()[-1])\
                                              for lang in texts.values()])
@logger_decorator_msg
def set_new_category(message: types.Message) -> None:
    """
    
    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    dish_uuid = message.reply_to_message.text.split()[-1]
    msg.edit_dish("category", dish_uuid)
    bot.send_message(user_id, texts[lang_code]["CAT_SET_MSG"])


@bot.message_handler(func=lambda message: message.reply_to_message \
                                          and message.reply_to_message.text \
                                          in [lang["EDIT_DESCRIPTION_MSG"](message.reply_to_message.text.split()[-1]) \
                                              for lang in texts.values()])
@logger_decorator_msg
def set_new_description(message: types.Message) -> None:
    """

    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    dish_uuid = message.reply_to_message.text.split()[-1]
    msg.edit_dish("dish_description", dish_uuid)
    bot.send_message(user_id, texts[lang_code]["DESC_SET_MSG"])


@bot.message_handler(func=lambda message: message.reply_to_message \
                                          and message.reply_to_message.text \
                                          in [lang["EDIT_PRICE_MSG"](message.reply_to_message.text.split()[-1]) \
                                              for lang in texts.values()])
@logger_decorator_msg
def set_new_price(message: types.Message) -> None:
    """

    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    dish_uuid = message.reply_to_message.text.split()[-1]
    msg.edit_dish("dish_price", dish_uuid)
    bot.send_message(user_id, texts[lang_code]["PRICE_SET_MSG"])


@bot.message_handler(commands=["delete_dish"])
@logger_decorator_msg
def delete_dish_command(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_rest_lang()
    user_id = msg.user_id
    bot.send_message(user_id,
                     texts[lang_code]["DELETE_DISH_SELECT_MSG"],
                     reply_markup=restaurant_menus.edit_dish_menu(lang_code, msg))


@bot.callback_query_handler(func=lambda call: call.message.text\
                                              in [lang["DELETE_DISH_SELECT_MSG"] for lang in texts.values()])
@logger_decorator_callback
def dish_deletion_select(call: types.CallbackQuery) -> None:
    """

    Args:
        call:

    Returns:

    """  # TODO
    c_back = DBInterface(call)
    lang_code = c_back.get_rest_lang()
    user_id = c_back.user_id
    message_id = c_back.data_to_read.message.id
    bot.delete_message(user_id, message_id)
    c_back.delete_dish()
    bot.send_message(user_id,
                     texts[lang_code]["DISH_DELETED_MSG"])


def main():
    logger.info("The bot is running.")
    bot.infinity_polling()


if __name__ == "__main__":
    main()
