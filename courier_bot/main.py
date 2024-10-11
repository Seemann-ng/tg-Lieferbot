import telebot as tb
import telebot.types as types
from environs import Env

import courier_menus
from tools.logger_tool import logger, logger_decorator_msg, logger_decorator_callback
from courier_db_tools import Interface as DBInterface
from courier_translations import texts

env = Env()
env.read_env()

BOT_TOKEN = env.str("COURIER_BOT_TOKEN")

bot = tb.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
@logger_decorator_msg
def start(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_courier_lang()
    user_id = msg.courier_id
    if not msg.courier_in_db():
        bot.send_message(user_id, texts[lang_code]["ASK_REG_MSG"], reply_markup=types.ForceReply())
    else:
        bot.send_message(user_id, texts[lang_code]["WELCOME_MSG"])


@bot.message_handler(func=lambda message: message.reply_to_message\
                                          and message.reply_to_message.text\
                                          in [lang["ASK_REG_MSG"] for lang in texts.values()])
@logger_decorator_msg
def ask_registration(message: types.Message) -> None:
    """

    Args:
        message:

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_courier_lang()
    user_id = msg.courier_id
    user_name = msg.data_to_read.from_user.username
    admin_id = msg.get_support_id()
    bot.send_message(admin_id, texts[lang_code]["REG_REQ_MSG"](user_name, user_id, message.text))
    bot.send_message(user_id, texts[lang_code]["REG_REQ_SENT_MSG"])


@bot.message_handler(commands=["select_language"])
@logger_decorator_msg
def change_lang_menu(message: types.Message) -> None:
    """Open language select menu.

    Args:
        message: Command with language select request.

    """
    msg = DBInterface(message)
    lang_code = msg.get_courier_lang()
    courier_id = msg.data_to_read.from_user.id
    bot.send_message(courier_id, texts[lang_code]["LANG_SEL_MENU"])
    bot.send_message(courier_id,
                     texts[lang_code]["CHANGE_LANG_MSG"],
                     reply_markup=courier_menus.lang_sel_menu(lang_code))


@bot.callback_query_handler(func= lambda call: call.message.text\
                                               in [lang["CHANGE_LANG_MSG"] for lang in texts.values()])
@logger_decorator_callback
def lang_set(call: types.CallbackQuery) -> None:
    """Change bot interface language.

    Args:
        call: Callback query with selected language info.

    """
    c_back = DBInterface(call)
    courier_id = c_back.data_to_read.from_user.id
    message_id = c_back.data_to_read.message.id
    c_back.set_courier_lang()
    bot.delete_message(courier_id, message_id - 1)
    bot.delete_message(courier_id, message_id)
    bot.send_message(courier_id, texts[c_back.data_to_read.data]["LANG_SELECTED_MSG"])


@bot.message_handler(commands=["open_shift"])
@logger_decorator_msg
def open_shift_command(message: types.Message) -> None:
    """

    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_courier_lang()
    courier_id = msg.courier_id
    msg.open_shift()
    bot.send_message(courier_id, texts[lang_code]["OPEN_SHIFT_MSG"])


@bot.message_handler(commands=["close_shift"])
@logger_decorator_msg
def close_shift_command(message: types.Message) -> None:
    """

    Args:
        message: 

    Returns:

    """  # TODO
    msg = DBInterface(message)
    lang_code = msg.get_courier_lang()
    courier_id = msg.courier_id
    msg.close_shift()
    bot.send_message(courier_id, texts[lang_code]["CLOSE_SHIFT_MSG"])


def main():
    logger.info("Bot is running")
    bot.infinity_polling()


if __name__ == '__main__':
    main()
