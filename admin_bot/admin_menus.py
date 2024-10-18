import telebot.types as types

from admin_translations import texts


# Restaurant accept order menu.
def rest_accept_order_menu(lang_code: str, order_uuid: str) -> types.InlineKeyboardMarkup:
    """Compose "Accept order" menu for a Restaurant in Restaurant's language.

    Args:
        lang_code: Restaurant's language.
        order_uuid: Order UUID.

    Returns:
        "Accept order" menu in required language.

    """
    menu = types.InlineKeyboardMarkup(row_width=1)
    accept_button = types.InlineKeyboardButton(text=texts[lang_code]["REST_ACCEPT_ORDER_BTN"],
                                               callback_data="accepted " + order_uuid)
    menu.add(accept_button)
    return menu
