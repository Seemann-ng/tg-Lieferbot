texts = {
    "en_US": {
        "PAYMENT_CONFIRMED_MSG": lambda order_uuid: f"Payment for order\n{order_uuid}\nconfirmed.",
        "REST_NEW_ORDER_MSG": lambda order_uuid, dishes, subtotal: f"New incoming order\n"\
                                                                   f"{order_uuid}\n"\
                                                                   f"Dishes:\n"\
                                                                   f"{dishes}\n"\
                                                                   f"To be paid:\n"\
                                                                   f"{subtotal}",
        "CUS_PAYMENT_CONFIRMED_MSG": lambda order_uuid: f"Payment for order\n"\
                                                        f"{order_uuid}\n"\
                                                        f"confirmed",
        "REST_ACCEPT_ORDER_BTN": "Accept order"
    },
    "de_DE": {
        "PAYMENT_CONFIRMED_MSG": lambda order_uuid: f"Payment for order\n{order_uuid}\nconfirmed.",
        "REST_NEW_ORDER_MSG": lambda order_uuid, dishes, subtotal: f"New incoming order\n"\
                                                                   f"{order_uuid}\n"\
                                                                   f"Dishes:\n"\
                                                                   f"{dishes}\n"\
                                                                   f"To be paid:\n"\
                                                                   f"{subtotal}",
        "CUS_PAYMENT_CONFIRMED_MSG": lambda order_uuid: f"Payment for order\n"\
                                                        f"{order_uuid}\n"\
                                                        f"confirmed",
        "REST_ACCEPT_ORDER_BTN": "Accept order"
    },
    "ru_RU": {
        "PAYMENT_CONFIRMED_MSG": lambda order_uuid: f"Payment for order\n{order_uuid}\nconfirmed.",
        "REST_NEW_ORDER_MSG": lambda order_uuid, dishes, subtotal: f"New incoming order\n"\
                                                                   f"{order_uuid}\n"\
                                                                   f"Dishes:\n"\
                                                                   f"{dishes}\n"\
                                                                   f"To be paid:\n"\
                                                                   f"{subtotal}",
        "CUS_PAYMENT_CONFIRMED_MSG": lambda order_uuid: f"Payment for order\n"\
                                                        f"{order_uuid}\n"\
                                                        f"confirmed",
        "REST_ACCEPT_ORDER_BTN": "Accept order"
    }
}