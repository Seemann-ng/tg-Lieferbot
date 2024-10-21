import telebot.types as types

from customer_translations import texts
from customer_db_tools import Interface as DBInterface

# Some common buttons here.
main_menu_button = lambda lang_code: types.KeyboardButton(text=texts[lang_code]["MAIN_MENU_BTN"])
back_button = lambda lang_code: types.InlineKeyboardButton(text=texts[lang_code]["GO_BACK_BTN"],
                                                           callback_data=texts[lang_code]["GO_BACK_BTN"])
cart_button = lambda lang_code: types.InlineKeyboardButton(text=texts[lang_code]["CART_BTN"],
                                                           callback_data=texts[lang_code]["CART_BTN"])
cancel_order_button = lambda lang_code: types.InlineKeyboardButton(text=texts[lang_code]["CANCEL_ORDER_BTN"],
                                                                   callback_data=texts[lang_code]["CANCEL_ORDER_BTN"])


# Agreement menu.
def agreement_menu(lang_code: str) -> types.ReplyKeyboardMarkup:
    """Compose "Accept Customer's agreement" menu in Customer's chosen language.

    Args:
        lang_code: Language code of the chosen language.

    Returns:
        "Accept Customer's agreement" menu in required language.

    """
    show_agreement_button = types.KeyboardButton(text=texts[lang_code]["SHOW_AGREEMENT_BTN"])
    accept_agreement_button = types.KeyboardButton(text=texts[lang_code]["ACCEPT_AGREEMENT_BTN"])
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                     input_field_placeholder=texts[lang_code]["AGREEMENT_MENU_PLACEHOLDER"])
    menu.add(show_agreement_button, accept_agreement_button)
    return menu


# Registration, phone number import method menu.
def reg_phone_menu(lang_code: str) -> types.ReplyKeyboardMarkup:
    """Compose "Choose phone number input method" menu in Customer's chosen language.

    Args:
        lang_code: Language code of the chosen language.

    Returns:
        "Choose phone number input method" menu in required language.

    """
    reg_phone_import_button = types.KeyboardButton(text=texts[lang_code]["REG_PHONE_IMPORT_BTN"], request_contact=True)
    reg_phone_str_button = types.KeyboardButton(text=texts[lang_code]["REG_PHONE_MAN_BTN"])
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                     input_field_placeholder=texts[lang_code]["REG_PHONE_MENU_PLACEHOLDER"])
    menu.add(reg_phone_import_button, reg_phone_str_button)
    return menu


# Registration, location menu.
def reg_location_menu(lang_code: str) -> types.ReplyKeyboardMarkup:
    """Compose "Share location" menu in Customer's chosen language.

    Args:
        lang_code: Language code of the chosen language.

    Returns:
        "Share location" menu in required language.

    """
    reg_location_button = types.KeyboardButton(text=texts[lang_code]["REG_LOCATION_BTN"], request_location=True)
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                     input_field_placeholder=texts[lang_code]["REG_LOCATION_PLACEHOLDER"])
    menu.add(reg_location_button)
    return menu


# Main menu.
def main_menu(lang_code: str) -> types.ReplyKeyboardMarkup:
    """Compose a main menu in Customer's chosen language.

    Args:
        lang_code: Language code of the chosen language.

    Returns:
        Main menu in requested language.

    """
    new_order_button = types.KeyboardButton(text=texts[lang_code]["NEW_ORDER_BTN"])
    my_orders_button = types.KeyboardButton(text=texts[lang_code]["MY_ORDERS_BTN"])
    options_button = types.KeyboardButton(text=texts[lang_code]["OPTIONS_BTN"])
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True)
    menu.add(new_order_button, my_orders_button)
    menu.add(options_button)
    return menu


# Options menu.
def options_menu(lang_code: str) -> types.ReplyKeyboardMarkup:
    """Compose options menu in Customer's chosen language.

    Args:
        lang_code: Language code of the chosen language.

    Returns:
        options menu in required language.

    """
    change_lang_button = types.InlineKeyboardButton(text=texts[lang_code]["CHANGE_LANG_BTN"])
    contact_support_button = types.KeyboardButton(text=texts[lang_code]["CONTACT_SUPPORT_BTN"])
    reset_contact_info_button = types.KeyboardButton(text=texts[lang_code]["RESET_CONTACT_INFO_BTN"])
    delete_profile_button = types.KeyboardButton(text=texts[lang_code]["DELETE_PROFILE_BTN"])
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                     input_field_placeholder=texts[lang_code]["OPTIONS_BTN"])
    menu.add(main_menu_button(lang_code))
    menu.add(change_lang_button)
    menu.add(contact_support_button)
    menu.add(reset_contact_info_button, delete_profile_button)
    return menu


# Reset contact info confirm menu.
def reset_info_menu(lang_code: str) -> types.ReplyKeyboardMarkup:
    """Compose "Reset profile info" menu in Customer's chosen language.

    Args:
        lang_code: Language code of the chosen language.

    Returns:
        "Reset profile info" menu in required language.

    """
    confirm_contact_info_reset_button = types.KeyboardButton(text=texts[lang_code]["CONFIRM_RESET_BTN"])
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                     input_field_placeholder=texts[lang_code]["RESET_CONTACT_INFO_BTN"] + "?")
    menu.add(main_menu_button(lang_code))
    menu.add(confirm_contact_info_reset_button)
    return menu


# Delete profile confirm menu.
def confirm_delete_profile_menu(lang_code: str) -> types.ReplyKeyboardMarkup:
    """Compose "Delete profile info" menu in Customer's chosen language.

    Args:
        lang_code: Language code of the chosen language.

    Returns:
        "Delete profile info" menu in required language.

    """
    confirm_delete_button = types.KeyboardButton(text=texts[lang_code]["CONFIRM_DELETE_PROFILE_BTN"])
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                     input_field_placeholder=texts[lang_code]["DELETE_PROFILE_BTN"] + "?")
    menu.add(main_menu_button(lang_code))
    menu.add(confirm_delete_button)
    return menu


# Confirm location menu.
def confirm_location_menu(lang_code: str) -> types.InlineKeyboardMarkup:
    """Compose "Confirm location" menu in Customer's chosen language.

    Args:
        lang_code: Language code of the chosen language.

    Returns:
        "Confirm location" menu in required language.

    """
    conf_loc_button = types.InlineKeyboardButton(text=texts[lang_code]["CONFIRM_LOCATION_BTN"],
                                                 callback_data=texts[lang_code]["CONFIRM_LOCATION_BTN"])
    wrong_loc_button = types.InlineKeyboardButton(text=texts[lang_code]["WRONG_LOCATION_BTN"],
                                                  callback_data=texts[lang_code]["WRONG_LOCATION_BTN"])
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(conf_loc_button, wrong_loc_button)
    return menu


# Choose restaurant type menu.
def choose_rest_type_menu(lang_code: str) -> types.InlineKeyboardMarkup:
    """Compose "Choose restaurant type" menu in Customer's chosen language.

    Args:
        lang_code: Language code of the chosen language.

    Returns:
        "Choose restaurant type" menu in required language.

    """
    menu = types.InlineKeyboardMarkup(row_width=1)
    if restaurant_types := DBInterface.show_restaurant_types():
        for restaurant_type in restaurant_types:
            menu.add(types.InlineKeyboardButton(text=restaurant_type[0], callback_data=restaurant_type[0]))
    menu.add(back_button(lang_code))
    return menu


# Choose restaurant menu.
def choose_rest_menu(lang_code: str, c_back: DBInterface) -> types.InlineKeyboardMarkup:
    """Compose "Choose restaurant" menu in Customer's chosen language.

    Args:
        lang_code: Language code of the chosen language.
        c_back: DBInterface object containing data regarding Customer's chosen restaurant type.

    Returns:
        "Choose restaurant" menu in required language.

    """
    menu = types.InlineKeyboardMarkup(row_width=1)
    if restaurants := c_back.show_restaurants():
        for restaurant in restaurants:
            menu.add(types.InlineKeyboardButton(text=restaurant[0], callback_data=restaurant[1]))
    menu.add(back_button(lang_code))
    return menu


# Choose dish category menu.
def choose_dish_cat_menu(lang_code: str, c_back: DBInterface) -> types.InlineKeyboardMarkup:
    """Compose "Choose dish category" menu in Customer's chosen language.

    Args:
        lang_code: Language code of the chosen language.
        c_back: DBInterface object containing data regarding Customer's chosen restaurant.

    Returns:
        "Choose dish category" menu in required language.

    """
    menu = types.InlineKeyboardMarkup(row_width=1)
    if dish_categories := c_back.show_dish_categories():
        for category in dish_categories:
            menu.add(types.InlineKeyboardButton(text=category[0], callback_data=category[0]))
    menu.add(cart_button(lang_code))
    if c_back.data_to_read.message.text != texts[lang_code]["ADD_MORE_BTN"]:
        menu.add(back_button(lang_code))
    menu.add(cancel_order_button(lang_code))
    return menu


# Choose dish menu.
def choose_dish_menu(lang_code: str, c_back: DBInterface) -> types.InlineKeyboardMarkup:
    """Compose "Choose dish" menu in Customer's chosen language.

    Args:
        lang_code: Language code of the chosen language.
        c_back: DBInterface object containing data regarding Customer's chosen dish category.

    Returns:
        "Choose dish" menu in required language.

    """
    menu = types.InlineKeyboardMarkup(row_width=1)
    if dishes := c_back.show_dishes():
        for dish in dishes:
            menu.add(types.InlineKeyboardButton(text=dish[0], callback_data=dish[1]))
    menu.add(cart_button(lang_code))
    menu.add(back_button(lang_code))
    menu.add(cancel_order_button(lang_code))
    return menu


# Dish selection confirmation menu.
def conf_sel_dish_menu(lang_code: str, c_back: DBInterface) -> types.InlineKeyboardMarkup:
    """Compose "Confirm selected dish" menu in Customer's chosen language.

    Args:
        lang_code: Language code of the chosen language.
        c_back: DBInterface object containing data regarding Customer's chosen dish.

    Returns:
        "Confirm selected dish" menu in required language.

    """
    add_dish_button = types.InlineKeyboardButton(text=texts[lang_code]["ADD_DISH_BTN"],
                                                 callback_data=c_back.data_to_read.data)
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(back_button(lang_code), add_dish_button)
    return menu


# Cart menu.
def cart_menu(lang_code: str) -> types.InlineKeyboardMarkup:
    """Compose "Cart" menu in Customer's chosen language.

    Args:
        lang_code: Language code of the chosen language.

    Returns:
        "Cart" menu in required language.

    """
    pay_button = types.InlineKeyboardButton(text=texts[lang_code]["MAKE_ORDER_BTN"],
                                            callback_data=texts[lang_code]["MAKE_ORDER_BTN"])
    add_more_button = types.InlineKeyboardButton(text=texts[lang_code]["ADD_MORE_BTN"],
                                                 callback_data=texts[lang_code]["ADD_MORE_BTN"])
    delete_item_button = types.InlineKeyboardButton(text=texts[lang_code]["DELETE_ITEM_BTN"],
                                                    callback_data=texts[lang_code]["DELETE_ITEM_BTN"])
    menu = types.InlineKeyboardMarkup(row_width=1)
    menu.add(pay_button, add_more_button, delete_item_button, cancel_order_button(lang_code))
    return menu


# Item deletion menu.
def item_deletion_menu(lang_code: str, c_back: DBInterface) -> types.InlineKeyboardMarkup:
    """Compose "Item deletion" menu in Customer's chosen language.

    Args:
        lang_code: Language code of the chosen language.
        c_back: DBInterface object containing data regarding Customer.

    Returns:
        "Item deletion" menu in required language.

    """
    menu = types.InlineKeyboardMarkup(row_width=1)
    if dishes_uuids := c_back.get_from_cart("dishes_uuids"):
        dishes_uuids = sorted(dishes_uuids)
        for dish_uuid in dishes_uuids:
            c_back.data_to_read.data = dish_uuid
            dish_name = c_back.get_dish()[0]
            menu.add(types.InlineKeyboardButton(text=dish_name, callback_data=dish_uuid))
    menu.add(cart_button(lang_code))
    return menu


# Select language menu.
def lang_sel_menu(lang_code: str) -> types.InlineKeyboardMarkup:
    """Compose "Language selection" menu in Customer's chosen language.

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


# Payment menu.
def payment_menu(lang_code: str, order_uuid: str) -> types.InlineKeyboardMarkup:
    """Compose "Payment" menu in Customer's chosen language.'

    Args:
        lang_code: Customer's language code.
        order_uuid: Order UUID.

    Returns:
        "Payment" menu in required language.

    """
    menu = types.InlineKeyboardMarkup(row_width=1)
    paid_button = types.InlineKeyboardButton(text=texts[lang_code]["PAID_BTN"],
                                             callback_data="paid " + order_uuid)
    cancel_button = types.InlineKeyboardButton(text=texts[lang_code]["CANCEL_ORDER_BTN"],
                                               callback_data="cancel " + order_uuid)
    menu.add(paid_button, cancel_button)
    return menu


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
