import telebot.types as types

from courier_translations import texts

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


# Restaurant order ready menu.
def rest_order_ready_menu(rest_lang: str, order_uuid: str) -> types.InlineKeyboardMarkup:
    """

    Args:
        rest_lang:
        order_uuid:

    Returns:

    """
    menu = types.InlineKeyboardMarkup(row_width=1)
    ready_button = types.InlineKeyboardButton(text=texts[rest_lang]["REST_READY_BTN"],
                                              callback_data="ready " + order_uuid)
    menu.add(ready_button)
    return menu


# Courier order in delivery menu.
def order_in_delivery_menu(courier_lang: str, order_uuid: str) -> types.InlineKeyboardMarkup:
    """

    Args:
        courier_lang:
        order_uuid:

    Returns:

    """
    menu = types.InlineKeyboardMarkup(row_width=1)
    delivered_button = types.InlineKeyboardButton(text=texts[courier_lang]["DELIVERED_BTN"],
                                                  callback_data="delivered " + order_uuid)
    menu.add(delivered_button)
    return menu


# Customer order delivered menu.
def cus_delivered_menu(customer_lang: str, order_uuid: str) -> types.InlineKeyboardMarkup:
    """

    Args:
        customer_lang:
        order_uuid:

    Returns:

    """
    menu = types.InlineKeyboardMarkup(row_width=1)
    order_closed_button = types.InlineKeyboardButton(text=texts[customer_lang]["ORDER_CLOSED_BTN"],
                                                     callback_data="order_closed " + order_uuid)
    menu.add(order_closed_button)
    return menu
