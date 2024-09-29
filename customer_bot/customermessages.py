WELCOME_BACK_MSG = "Welcome back, "
MAIN_MENU_MSG = "You're in main menu now."
FIRST_WELCOME_MSG = "Welcome to the %BOT_NAME%."
ASK_AGREEMENT_MSG = "To proceed, You have to accept our Customer Agreement."
AGREEMENT_TEXT = "SAMPLE AGREEMENT TEXT."
AGREEMENT_ACCEPTED_MSG = "Customer Agreement was accepted."
REG_NAME_MSG = "How can I call You?"
REG_NAME_PLACEHOLDER = "Your name"
REG_NAME_RECEIVED_MSG = "Your name has been changed to: "
REG_PHONE_METHOD_MSG = "How would You like to provide your phone number?"
REG_PHONE_MSG = "Please provide us Your phone number (without '+49'!)."
REG_PHONE_PLACEHOLDER = "Your phone number"
PHONE_RECEIVED_MSG = "Your phone number has been changed to: "
INVALID_PHONE_MSG = "Invalid phone number."
REG_LOCATION_MSG = "Please send Your location."
REG_LOCATION_RECEIVED_MSG = "Your current location is:"
OPTIONS_MSG = "Here You can contact Support, reset or delete Your contact info."
RESET_CONTACT_INFO_MSG = "Are You sure You want to reset Your contact info?"
CONTACT_INFO_DELETED_MSG = "Your contact info were deleted."
DELETE_PROFILE_MSG = "Are You sure You want to delete Your profile?"
PROFILE_DELETED_MSG = "Your profile has been deleted."


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
           f"Total: €{total}\n"
           f"Date: {order_date}\n"
           f"Status: {order_status}\n")
    return msg


