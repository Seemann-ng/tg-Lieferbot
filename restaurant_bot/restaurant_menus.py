import telebot.types as types

from restaurant_translations import texts
from restaurant_db_tools import Interface as DBInterface

back_button = lambda lang_code: types.InlineKeyboardButton(text=texts[lang_code]["GO_BACK_BTN"],
                                                           callback_data=texts[lang_code]["GO_BACK_BTN"])


def edit_dish_menu(lang_code: str, msg: DBInterface) -> types.InlineKeyboardMarkup:
    """

    Args:
        lang_code:
        msg:

    Returns:

    """  # TODO
    dishes = msg.get_dishes()
    menu = types.InlineKeyboardMarkup(row_width=1)
    for dish in dishes:
        dish_button = types.InlineKeyboardButton(text=dish[1], callback_data=dish[0])
        menu.add(dish_button)
    menu.add(back_button(lang_code))
    return menu


def edit_dish_param_menu(lang_code: str, c_back: DBInterface) -> types.InlineKeyboardMarkup:
    """
    
    Args:
        lang_code: 
        c_back: 

    Returns:

    """  # TODO
    dish_uuid = c_back.data_to_read.data
    cat_button = types.InlineKeyboardButton(text=texts[lang_code]["EDIT_CAT_BTN"], callback_data="cat "+dish_uuid)
    descr_button = types.InlineKeyboardButton(text=texts[lang_code]["EDIT_DESC_BTN"], callback_data="des "+dish_uuid)
    price_button = types.InlineKeyboardButton(text=texts[lang_code]["EDIT_PRICE_BTN"], callback_data="prc "+dish_uuid)
    menu = types.InlineKeyboardMarkup(row_width=1)
    menu.add(cat_button, descr_button, price_button, back_button(lang_code))
    return menu


def lang_sel_menu(lang_code: str) -> types.InlineKeyboardMarkup:
    """Compose "Language selection" menu in chosen language.

    Args:
        lang_code: Language code of the chosen language.

    Returns:
        "Language selection" menu in required language.

    """
    menu = types.InlineKeyboardMarkup(row_width=1)
    de_button = types.InlineKeyboardButton(text=texts[lang_code]["SEL_LANG_DE_BTN"], callback_data="de_DE")
    en_button = types.InlineKeyboardButton(text=texts[lang_code]["SEL_LANG_EN_BTN"], callback_data="en_US")
    ru_button = types.InlineKeyboardButton(text=texts[lang_code]["SEL_LANG_RU_BTN"], callback_data="ru_RU")
    menu.add(de_button, en_button, ru_button)
    return menu


# Courier accept order menu.
def courier_accept_menu(order_uuid: str, lang_code: str) -> types.InlineKeyboardMarkup:
    """

    Args:
        order_uuid:
        lang_code:

    Returns:

    """
    menu = types.InlineKeyboardMarkup(row_width=1)
    accept_button = types.InlineKeyboardButton(text=texts[lang_code]["COURIER_ACCEPT_BTN"],
                                               callback_data="accept " + order_uuid)
    menu.add(accept_button)
    return menu
