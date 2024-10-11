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