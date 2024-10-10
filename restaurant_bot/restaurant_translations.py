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
        "LANG_SEL_MENU": "Bot language selection menu.",
        "CHANGE_LANG_MSG": "Select bot language",
        "SEL_LANG_DE_BTN": "🇩🇪 German\n(Deutsch)",
        "SEL_LANG_EN_BTN": "🇺🇸 English",
        "SEL_LANG_RU_BTN": "🇷🇺 Russian\n(Русский)",
        "LANG_SELECTED_MSG": "Language changed to English!",
        "OPEN_SHIFT_MSG": "Shift is opened, now You can receive orders.",
        "CLOSE_SHIFT_MSG": "Shift is closed.",
        "DISH_AVAILABLE_SELECT_MSG": "Choose dish to make it available.",
        "DISH_SET_AVAILABLE_MSG": "Selected dish has been set available.",
        "DISH_UNAVAILABLE_SELECT_MSG": "Choose dish to make it unavailable.",
        "DISH_SET_UNAVAILABLE_MSG": "Selected dish has been set unavailable.",
        "DELETE_DISH_SELECT_MSG": "Select dish to delete.",
        "DISH_DELETED_MSG": "Selected dish has been deleted.",
        "DISH_ADDED_MSG": lambda dish_name: f"Dish: {dish_name} has been added to the Database.",
        "EDIT_DISH_MSG": "Choose a dish to edit",
        "GO_BACK_BTN": "BACK",
        "EDIT_DISH_CHOSEN_MSG": lambda dish_name: f"Dish to edit:\n{dish_name}",
        "EDIT_DISH_PARAM_MSG": "Which parameter of the dish do You want to change?",
        "EDIT_DESC_BTN": "Description IN DEV",
        "EDIT_CAT_BTN": "Category IN DEV",
        "EDIT_PRICE_BTN": "Price IN DEV",
        "EDIT_CATEGORY_MSG": lambda dish_uuid: f"Enter new category for the dish:\n"\
                                               f"Dish UUID: {dish_uuid}",
        "CAT_SET_MSG": "New category has been set for the dish.",
        "EDIT_DESCRIPTION_MSG": lambda dish_uuid: f"Enter new description for the dish:\n"\
                                                  f"Dish UUID: {dish_uuid}",
        "DESC_SET_MSG": "New description has been set for the dish.",
        "EDIT_PRICE_MSG": lambda dish_uuid: f"Enter new price for the dish:\n"\
                                            f"Dish UUID: {dish_uuid}",
        "PRICE_SET_MSG": "New price has been set for the dish.",
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
        "LANG_SEL_MENU": "Bot language selection menu.",
        "CHANGE_LANG_MSG": "Select bot language",
        "SEL_LANG_DE_BTN": "🇩🇪 German\n(Deutsch)",
        "SEL_LANG_EN_BTN": "🇺🇸 English",
        "SEL_LANG_RU_BTN": "🇷🇺 Russian\n(Русский)",
        "LANG_SELECTED_MSG": "Language changed to English!",
        "OPEN_SHIFT_MSG": "Shift is opened, now You can receive orders.",
        "CLOSE_SHIFT_MSG": "Shift is closed.",
        "DISH_AVAILABLE_SELECT_MSG": "Choose dish to make it available.",
        "DISH_SET_AVAILABLE_MSG": "Selected dish has been set available.",
        "DISH_UNAVAILABLE_SELECT_MSG": "Choose dish to make it unavailable.",
        "DISH_SET_UNAVAILABLE_MSG": "Selected dish has been set unavailable.",
        "DELETE_DISH_SELECT_MSG": "Select dish to delete.",
        "DISH_DELETED_MSG": "Selected dish has been deleted.",
        "DISH_ADDED_MSG": lambda dish_name: f"Dish: {dish_name} has been added to the Database.",
        "EDIT_DISH_MSG": "Choose a dish to edit",
        "GO_BACK_BTN": "BACK",
        "EDIT_DISH_CHOSEN_MSG": lambda dish_name: f"Dish to edit:\n{dish_name}",
        "EDIT_DISH_PARAM_MSG": "Which parameter of the dish do You want to change?",
        "EDIT_DESC_BTN": "Description",
        "EDIT_CAT_BTN": "Category",
        "EDIT_PRICE_BTN": "Price",
        "EDIT_CATEGORY_MSG": lambda dish_uuid: f"Enter new category for the dish:\n"\
                                               f"Dish UUID: {dish_uuid}",
        "CAT_SET_MSG": "New category has been set for the dish.",
        "EDIT_DESCRIPTION_MSG": lambda dish_uuid: f"Enter new description for the dish:\n"\
                                                  f"Dish UUID: {dish_uuid}",
        "DESC_SET_MSG": "New description has been set for the dish.",
        "EDIT_PRICE_MSG": lambda dish_uuid: f"Enter new price for the dish:\n"\
                                            f"Dish UUID: {dish_uuid}",
        "PRICE_SET_MSG": "New price has been set for the dish.",
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
        "LANG_SEL_MENU": "Bot language selection menu.",
        "CHANGE_LANG_MSG": "Select bot language",
        "SEL_LANG_DE_BTN": "🇩🇪 German\n(Deutsch)",
        "SEL_LANG_EN_BTN": "🇺🇸 English",
        "SEL_LANG_RU_BTN": "🇷🇺 Russian\n(Русский)",
        "LANG_SELECTED_MSG": "Language changed to English!",
        "OPEN_SHIFT_MSG": "Shift is opened, now You can receive orders.",
        "CLOSE_SHIFT_MSG": "Shift is closed.",
        "DISH_AVAILABLE_SELECT_MSG": "Choose dish to make it available.",
        "DISH_SET_AVAILABLE_MSG": "Selected dish has been set available.",
        "DISH_UNAVAILABLE_SELECT_MSG": "Choose dish to make it unavailable.",
        "DISH_SET_UNAVAILABLE_MSG": "Selected dish has been set unavailable.",
        "DELETE_DISH_SELECT_MSG": "Select dish to delete.",
        "DISH_DELETED_MSG": "Selected dish has been deleted.",
        "DISH_ADDED_MSG": lambda dish_name: f"Dish: {dish_name} has been added to the Database.",
        "EDIT_DISH_MSG": "Choose a dish to edit",
        "GO_BACK_BTN": "BACK",
        "EDIT_DISH_CHOSEN_MSG": lambda dish_name: f"Dish to edit:\n{dish_name}",
        "EDIT_DISH_PARAM_MSG": "Which parameter of the dish do You want to change?",
        "EDIT_DESC_BTN": "Description",
        "EDIT_CAT_BTN": "Category",
        "EDIT_PRICE_BTN": "Price",
        "EDIT_CATEGORY_MSG": lambda dish_uuid: f"Enter new category for the dish:\n"\
                                               f"Dish UUID: {dish_uuid}",
        "CAT_SET_MSG": "New category has been set for the dish.",
        "EDIT_DESCRIPTION_MSG": lambda dish_uuid: f"Enter new description for the dish:\n"\
                                                  f"Dish UUID: {dish_uuid}",
        "DESC_SET_MSG": "New description has been set for the dish.",
        "EDIT_PRICE_MSG": lambda dish_uuid: f"Enter new price for the dish:\n"\
                                            f"Dish UUID: {dish_uuid}",
        "PRICE_SET_MSG": "New price has been set for the dish.",
    }
}