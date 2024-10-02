import telebot.types as types

# Button textes.
AGREEMENT_MENU_PLACEHOLDER = "📑 Agreement"
SHOW_AGREEMENT_BTN = "🔍📑 Show Customer Agreement"
ACCEPT_AGREEMENT_BTN = "📝 Accept Customer Agreement"
REG_PHONE_MENU_PLACEHOLDER = "📱 Phone number input"
REG_PHONE_MAN_BTN = "👨🏼‍💻 Input phone number manually"
REG_PHONE_IMPORT_BTN = "⬆️ Import phone number from account"
REG_LOCATION_BTN = "🌍 Send location"
REG_LOCATION_PLACEHOLDER = "🌍 Location"
MAIN_MENU_BTN = "🟰 Main Menu"
NEW_ORDER_BTN = "⭕️ New Order"
MY_ORDERS_BTN = "📑 My Orders"
OPTIONS_BTN = "🟰 Options"
CONTACT_SUPPORT_BTN = "📞 Contact support (in development)."
RESET_CONTACT_INFO_BTN = "⚠️ Reset Contact Info"
CONFIRM_RESET_BTN = "✅ YES, reset my contact info"
DELETE_PROFILE_BTN = "⚠️ Delete profile"
CONFIRM_DELETE_PROFILE_BTN = "✅ YES, delete my profile"
CONFIRM_LOCATION_BTN = "✅ Yes!"
WRONG_LOCATION_MSG = "❌ No."
GO_BACK_BTN = "⬅️ Go back"
CART_BTN = "🛒 My cart"
CANCEL_ORDER_BTN = "🚫 CANCEL ORDER"
ADD_DISH_BTN = "✅ Add to cart"
PAY_BTN = "💳 Confirm order"
ADD_MORE_BTN = "🛍 Continue shopping"
DELETE_ITEM_BTN = "📤 Delete item"

# Agreement menu.
show_agreement_button = types.KeyboardButton(text=SHOW_AGREEMENT_BTN)
accept_agreement_button = types.KeyboardButton(text=ACCEPT_AGREEMENT_BTN)
agreement_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder=AGREEMENT_MENU_PLACEHOLDER)
agreement_menu.add(show_agreement_button, accept_agreement_button)

# Registration, phone number import method menu.
reg_phone_import_button = types.KeyboardButton(text=REG_PHONE_IMPORT_BTN, request_contact=True)
reg_phone_str_button = types.KeyboardButton(text=REG_PHONE_MAN_BTN)
reg_phone_menu = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder=REG_PHONE_MENU_PLACEHOLDER
)
reg_phone_menu.add(reg_phone_import_button, reg_phone_str_button)

# Registration, location menu.
reg_location_button = types.KeyboardButton(text=REG_LOCATION_BTN, request_location=True)
reg_location_menu = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder=REG_LOCATION_PLACEHOLDER
)
reg_location_menu.add(reg_location_button)

# Main menu.
new_order_button = types.KeyboardButton(text=NEW_ORDER_BTN)
my_orders_button = types.KeyboardButton(text=MY_ORDERS_BTN)
options_button = types.KeyboardButton(text=OPTIONS_BTN)
main_menu = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
)
main_menu.add(new_order_button, my_orders_button)
main_menu.add(options_button)

main_menu_button = types.KeyboardButton(text=MAIN_MENU_BTN)

# Options menu.
contact_support_button = types.KeyboardButton(text=CONTACT_SUPPORT_BTN)
reset_contact_info_button = types.KeyboardButton(text=RESET_CONTACT_INFO_BTN)
delete_profile_button = types.KeyboardButton(text=DELETE_PROFILE_BTN)
options_menu = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder=OPTIONS_BTN
)
options_menu.add(main_menu_button)
options_menu.add(contact_support_button)
options_menu.add(reset_contact_info_button, delete_profile_button)

# Reset contact info confirm menu.
confirm_contact_info_reset_button = types.KeyboardButton(text=CONFIRM_RESET_BTN)
reset_info_menu = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder=RESET_CONTACT_INFO_BTN+"?",
)
reset_info_menu.add(main_menu_button)
reset_info_menu.add(confirm_contact_info_reset_button)

# Delete profile confirm menu.
confirm_delete_button = types.KeyboardButton(text=CONFIRM_DELETE_PROFILE_BTN)
confirm_delete_profile_menu = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder=DELETE_PROFILE_BTN+"?"
)
confirm_delete_profile_menu.add(main_menu_button)
confirm_delete_profile_menu.add(confirm_delete_button)

# Confirm location menu.
confirm_location_button = types.InlineKeyboardButton(text=CONFIRM_LOCATION_BTN, callback_data=CONFIRM_LOCATION_BTN)
wrong_location_button = types.InlineKeyboardButton(text=WRONG_LOCATION_MSG, callback_data=WRONG_LOCATION_MSG)
confirm_location_menu = types.InlineKeyboardMarkup(row_width=2)
confirm_location_menu.add(confirm_location_button, wrong_location_button)

# Order creation menu buttons.
back_button = types.InlineKeyboardButton(text=GO_BACK_BTN, callback_data=GO_BACK_BTN)
cart_button = types.InlineKeyboardButton(text=CART_BTN, callback_data=CART_BTN)
cancel_order_button = types.InlineKeyboardButton(text=CANCEL_ORDER_BTN, callback_data=CANCEL_ORDER_BTN)
