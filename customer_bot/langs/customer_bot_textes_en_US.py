# Menu buttons.
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
CONTACT_SUPPORT_BTN = "📞 Contact support\n🛠IN DEVELOPMENT🛠"
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

# Localization variables.
PHONE_NUM_PREFIX = "+1"
MAX_PHONE_LENGTH_WO_PREFIX = 11
CURRENCY = "💲"

# Bot messages.
IN_DEV = "I've told You, IT IS IN DEVELOPMENT!"
WELCOME_BACK_MSG = "Welcome back, "
MAIN_MENU_MSG = "You're in main menu now."
FIRST_WELCOME_MSG = "Welcome to the %BOT_NAME%."
ASK_AGREEMENT_MSG = "To proceed, You have to accept our Customer Agreement."
AGREEMENT_TEXT = "SAMPLE AGREEMENT TEXT."
AGREEMENT_ACCEPTED_MSG = "✅ Customer Agreement was accepted."
REG_NAME_MSG = "How can I call You?"
REG_NAME_PLACEHOLDER = "Your name"
REG_NAME_RECEIVED_MSG = "Your name has been changed to: "
REG_PHONE_METHOD_MSG = "How would You like to provide your phone number?"
REG_PHONE_MSG = "Please provide us Your phone number (without '+49'!)."
REG_PHONE_PLACEHOLDER = "Your phone number"
PHONE_RECEIVED_MSG = "Your phone number has been changed to: "
INVALID_PHONE_MSG = "‼️ Invalid phone number."
REG_LOCATION_MSG = "Please send Your location."
REG_LOCATION_RECEIVED_MSG = "Your current location is:"
NO_ORDERS_FOUND_MSG = "😞 No orders were found."
OPTIONS_MSG = "Here You can contact Support, reset or delete Your contact info."
RESET_CONTACT_INFO_MSG = "⚠️ Are You sure You want to reset Your contact info?"
CONTACT_INFO_DELETED_MSG = " ⚠️Your contact info were deleted."
DELETE_PROFILE_MSG = "⚠️ Are You sure You want to delete Your profile?"
PROFILE_DELETED_MSG = "⚠️ Your profile has been deleted."
EXITING_ORDER_MENU_MSG = "Going back to main menu."
DELETING_CART_ALERT = "⚠️ Your cart was cleared."
GOING_BACK_MSG = "Going back..."
LOCATION_NOT_FOUND_MSG = f"Contact information wasn't found.\n"\
                         f"Please, reset Your contact information.\n"\
                         f"(\'{OPTIONS_BTN}\' => \'{RESET_CONTACT_INFO_BTN}\')"
REQUEST_NEW_LOCATION_MSG = f"Please, reset Your contact information.\n"\
                         f"(\'{OPTIONS_BTN}\' => \'{RESET_CONTACT_INFO_BTN}\')"
CONFIRM_LOCATION_MSG = "Is this delivery address right?"
CHOOSE_REST_TYPE_MSG = "Please, choose a restaurant type."
SELECTED_REST_TYPE_MSG = "Selected restaurant type:"
CHOOSE_REST_MSG = "Please, choose a restaurant."
SELECTED_REST_MSG = "Selected restaurant:"
CHOOSE_DISH_CATEGORY_MSG = "Please, choose a dish category."
SELECTED_DISH_CAT_MSG = "Selected dish category:"
CHOOSE_DISH_MSG = "Please, choose Your dish"
SELECTED_DISH_MSG = "Selected dish:"
DISH_DESC_MSG = "Description:"
DISH_PRICE_MSG = "Price:"
YOUR_CART_MSG = "🛒 Your cart:"
SUBTOTAL_MSG = "Subtotal"

# TODO: lambda
def my_orders_msg(orders: list) -> str:
    if not orders:
        return "You have no orders yet."
    order_id = orders[0][0][-6:]
    order_from = orders[0][1]
    courier_name = orders[0][2]
    dishes = orders[0][3]
    total = orders[0][4]
    order_date = orders[0][5]
    order_status = orders[0][6]
    orders.pop(0)
    msg = (f"Order Number: {order_id}\n"
           f"from: {order_from}\n"
           f"Courier: {courier_name}\n"
           f"Dish(es): {dishes}\n"
           f"Total: {CURRENCY}{total}\n"
           f"Date: {order_date}\n"
           f"Status: {order_status}\n")
    return msg
