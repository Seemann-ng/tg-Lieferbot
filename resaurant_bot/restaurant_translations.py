texts = {
    "en_US": {
        "ASK_REGISTRATION_MSG": "This Telegram account isn't registered as a Restaurant account.\n"
                                "Please contact support for registration by replying to this message.\n"
                                "(By replying You agree Your contact info i.e. Telegram ID and Username "
                                "to be provided to Our Support Service.)",
        "WELCOME_MSG": "Welcome to %RESTAURANT_BOT_NAME%!",
        "REG_REQUEST_MSG": lambda username, user_id, text: f"Incoming restaurant registration request\n"\
                                                           f"from @{username} ({user_id}):\n"\
                                                           f"{text}",
        "REG_REQUEST_SENT_MSG": "Your request has been sent to Our Support Service.",
        "DISH_ADDED_MSG": lambda dish_name: f"Dish: {dish_name} has been added to the Database.",
        "EDIT_DISH_MSG": "Choose a dish to edit",
        "GO_BACK_BTN": "BACK",
        "EDIT_DISH_CHOSEN_MSG": lambda dish_name: f"Dish to edit:\n{dish_name}",
        "EDIT_DISH_PARAM_MSG": "Which parameter of the dish do You want to change?",
        "EDIT_DESC_BTN": "Description IN DEV",
        "EDIT_CAT_BTN": "Category IN DEV",
        "EDIT_PRICE_BTN": "Price IN DEV",
    },
    "de_DE": {
        "ASK_REGISTRATION_MSG": "This Telegram account isn't registered as a Restaurant account.\n"
                                "Please contact support for registration by replying to this message.\n"
                                "(By replying You agree Your contact info i.e. Telegram ID and Username "
                                "to be provided to Our Support service.)",
        "WELCOME_MSG": "Welcome to %RESTAURANT_BOT_NAME%!",
        "REG_REQUEST_MSG": lambda username, user_id, text: f"Incoming restaurant registration request\n"\
                                                           f"from @{username} ({user_id}):\n"\
                                                           f"{text}",
        "REG_REQUEST_SENT_MSG": "Your request has been sent to Our Support Service.",
        "DISH_ADDED_MSG": lambda dish_name: f"Dish: {dish_name} has been added to the Database.",
        "EDIT_DISH_MSG": "Choose a dish to edit",
        "GO_BACK_BTN": "BACK",
        "EDIT_DISH_CHOSEN_MSG": lambda dish_name: f"Dish to edit:\n{dish_name}",
        "EDIT_DISH_PARAM_MSG": "Which parameter of the dish do You want to change?",
        "EDIT_DESC_BTN": "Description",
        "EDIT_CAT_BTN": "Category",
        "EDIT_PRICE_BTN": "Price"
    },
    "ru_RU": {
        "ASK_REGISTRATION_MSG": "This Telegram account isn't registered as a Restaurant account.\n"
                                "Please contact support for registration by replying to this message.\n"
                                "(By replying You agree Your contact info i.e. Telegram ID and Username "
                                "to be provided to Our Support service.)",
        "WELCOME_MSG": "Welcome to %RESTAURANT_BOT_NAME%!",
        "REG_REQUEST_MSG": lambda username, user_id, text: f"Incoming restaurant registration request\n"\
                                                           f"from @{username} ({user_id}):\n"\
                                                           f"{text}",
        "REG_REQUEST_SENT_MSG": "Your request has been sent to Our Support Service.",
        "DISH_ADDED_MSG": lambda dish_name: f"Dish: {dish_name} has been added to the Database.",
        "EDIT_DISH_MSG": "Choose a dish to edit",
        "GO_BACK_BTN": "BACK",
        "EDIT_DISH_CHOSEN_MSG": lambda dish_name: f"Dish to edit:\n{dish_name}",
        "EDIT_DISH_PARAM_MSG": "Which parameter of the dish do You want to change?",
        "EDIT_DESC_BTN": "Description",
        "EDIT_CAT_BTN": "Category",
        "EDIT_PRICE_BTN": "Price"
    }
}
