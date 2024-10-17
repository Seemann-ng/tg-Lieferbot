import telebot.types as types

from admin_translations import texts


# Restaurant accept order menu.
def rest_accept_order_menu(lang_code: str, order_uuid: str) -> types.InlineKeyboardMarkup:
    """

    Args:
        lang_code:
        order_uuid:

    Returns:

    """
    menu = types.InlineKeyboardMarkup(row_width=1)
    accept_button = types.InlineKeyboardButton(text=texts[lang_code]["REST_ACCEPT_ORDER_BTN"],
                                               callback_data="accepted " + order_uuid)
    menu.add(accept_button)
    return menu
