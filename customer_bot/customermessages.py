import customermenus

PHONE_NUM_PREFIX = "+49"
MAX_PHONE_LENGTH_WO_PREFIX = 11
CURRENCY = "€"
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
                         f"(\'{customermenus.OPTIONS_BTN}\' -> \'{customermenus.RESET_CONTACT_INFO_BTN}\')"
REQUEST_NEW_LOCATION_MSG = f"Please, reset Your contact information.\n"\
                         f"(\'{customermenus.OPTIONS_BTN}\' -> \'{customermenus.RESET_CONTACT_INFO_BTN}\')"
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

# TODO transfer button textes from /customermenus.py
