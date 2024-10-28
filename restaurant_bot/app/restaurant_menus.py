import telebot.types as types

from restaurant_translations import texts
from restaurant_db_tools import Interface as DBInterface

back_button = lambda lang_code: types.InlineKeyboardButton(
    text=texts[lang_code]["GO_BACK_BTN"],
    callback_data=texts[lang_code]["GO_BACK_BTN"]
)


def edit_dish_menu(lang_code: str, msg: DBInterface) -> types.InlineKeyboardMarkup:
    """Compose "edit dish" menu in Restaurant's language.

    Args:
        lang_code: Language code of the Restaurant's language.
        msg: DBInterface instance containing message from User.

    Returns:
        "Edit dish" menu in Restaurant's language.

    """
    menu = types.InlineKeyboardMarkup(row_width=1)
    for dish in msg.get_dishes():
        dish_button = types.InlineKeyboardButton(text=dish[1], callback_data=dish[0])
        menu.add(dish_button)
    menu.add(back_button(lang_code))
    return menu


def edit_dish_param_menu(lang_code: str, callback: DBInterface) -> types.InlineKeyboardMarkup:
    """Compose "edit dish parameter" menu in Restaurant's language.
    
    Args:
        lang_code: Language code of the Restaurant's language.
        callback: DBInterface instance containing callback query from
            User.

    Returns:
        "Edit dish parameter" menu in Restaurant's language.

    """
    cat_button = types.InlineKeyboardButton(
        text=texts[lang_code]["EDIT_CAT_BTN"],
        callback_data=f"cat {callback.data_to_read.data}"
    )
    descr_button = types.InlineKeyboardButton(
        text=texts[lang_code]["EDIT_DESC_BTN"],
        callback_data=f"des {callback.data_to_read.data}"
    )
    price_button = types.InlineKeyboardButton(
        text=texts[lang_code]["EDIT_PRICE_BTN"],
        callback_data=f"prc {callback.data_to_read.data}"
    )
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
    de_button = types.InlineKeyboardButton(
        text=texts[lang_code]["SEL_LANG_DE_BTN"],
        callback_data="de_DE"
    )
    en_button = types.InlineKeyboardButton(
        text=texts[lang_code]["SEL_LANG_EN_BTN"],
        callback_data="en_US"
    )
    ru_button = types.InlineKeyboardButton(
        text=texts[lang_code]["SEL_LANG_RU_BTN"],
        callback_data="ru_RU"
    )
    menu.add(de_button, en_button, ru_button)
    return menu


# Courier accept order menu.
def courier_accept_menu(order_uuid: str, lang_code: str) -> types.InlineKeyboardMarkup:
    """Compose "accept order" in courier's language.

    Args:
        order_uuid: Order UUID.
        lang_code: Language code of courier's language.

    Returns:
        "Accept order" menu in required language.

    """
    menu = types.InlineKeyboardMarkup(row_width=1)
    accept_button = types.InlineKeyboardButton(
        text=texts[lang_code]["COURIER_ACCEPT_BTN"],
        callback_data=f"accept {order_uuid}"
    )
    menu.add(accept_button)
    return menu


# Courier order in delivery menu.
def courier_in_delivery_menu(order_uuid: str, courier_lang: str) -> types.InlineKeyboardMarkup:
    """Compose "order in delivery" menu in courier's language.

    Args:
        order_uuid: Order UUID.
        courier_lang: Language code of courier's language.

    Returns:
        "Order in delivery" menu in required language.

    """
    menu = types.InlineKeyboardMarkup(row_width=1)
    order_handled_button = types.InlineKeyboardButton(
        text=texts[courier_lang]["COUR_ORDER_IN_DELIVERY_BTN"],
        callback_data=f"in_delivery {order_uuid}"
    )
    menu.add(order_handled_button)
    return menu
