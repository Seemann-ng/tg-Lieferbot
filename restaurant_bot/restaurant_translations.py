from environs import Env

env = Env()
env.read_env()

BOT_NAME = env.str("BRAND_NAME")

texts = {
    "en_US": {
        "ASK_REGISTRATION_MSG": "This Telegram account isn't registered as a Restaurant account.\n"
                                "Please contact support for registration by replying to this message.\n"
                                "(By replying You agree Your contact info i.e. Telegram ID and Username "
                                "to be provided to Our Support Service.)",
        "WELCOME_MSG": f"Welcome to {BOT_NAME}-Restaurant!",
        "REG_REQUEST_MSG": lambda
            username,
            user_id,
            text: f"❗️ Incoming restaurant registration request\n" \
                  f"from @{username} (`{user_id}`):\n" \
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
        "DISH_AVAILABLE_SELECT_MSG": "Choose item to make it available.",
        "DISH_SET_AVAILABLE_MSG": "Selected item has been set available.",
        "DISH_UNAVAILABLE_SELECT_MSG": "Choose item to make it unavailable.",
        "DISH_SET_UNAVAILABLE_MSG": "Selected item has been set unavailable.",
        "DELETE_DISH_SELECT_MSG": "Select item to delete.",
        "DISH_DELETED_MSG": "Selected item has been deleted.",
        "DISH_ADDED_MSG": lambda dish_name: f"✅ Item: {dish_name} has been added to the Database.",
        "NO_DISH_NAME_MSG": "No item name was provided.",
        "EDIT_DISH_MSG": "Choose a item to edit",
        "GO_BACK_BTN": "⬅️ BACK",
        "EDIT_DISH_CHOSEN_MSG": lambda dish_name: f"Item to edit:\n{dish_name}",
        "EDIT_DISH_PARAM_MSG": "Which parameter of the item do You want to change?",
        "EDIT_DESC_BTN": "📝 Description",
        "EDIT_CAT_BTN": "🛍 Category",
        "EDIT_PRICE_BTN": "💶 Price",
        "EDIT_CATEGORY_MSG": lambda
            dish_uuid: f"Enter new category for the item:\n" \
                       f"Item UUID: {dish_uuid}",
        "CAT_SET_MSG": "✅ New category has been set for the item.",
        "EDIT_DESCRIPTION_MSG": lambda
            dish_uuid: f"Enter new description for the item:\n" \
                       f"Item UUID: {dish_uuid}",
        "DESC_SET_MSG": "✅ New description has been set for the item.",
        "EDIT_PRICE_MSG": lambda
            dish_uuid: f"Enter new price for the item:\n" \
                       f"Item UUID: {dish_uuid}",
        "PRICE_SET_MSG": "✅ New price has been set for the item.",
        "REST_ORDER_ACCEPTED_MSG": lambda order_uuid: f"✅ Accepted order\n`{order_uuid}`",
        "CUST_ORDER_ACCEPTED_MSG": lambda
            order_uuid: f"Order\n`{order_uuid}`\n" \
                        f"Status update:\n" \
                        f"Order received by the restaurant, looking for a courier.",
        "LOOKING_FOR_COURIER_MSG": lambda
            order_uuid,
            courier_fee,
            customer_name,
            customer_username,
            customer_phone,
            comment,
            rest_name,
            dishes,
            rest_address: f"New incoming order:\n`{order_uuid}`\n" \
                          f"Courier pay:\n€`{courier_fee}`\n" \
                          f"Customer's name:\n{customer_name}\n" \
                          f"Customer's Telegram:\n @{customer_username}\n" \
                          f"Customer's phone:\n{customer_phone}\n" \
                          f"Order comments:\n{comment}\n" \
                          f"Restaurant:\n`{rest_name}`\n" \
                          f"Item(s):\n{dishes}\n" \
                          f"Restaurant address:\n`{rest_address}`\n" \
                          f"Restaurant location:",
        "COURIER_DELIVERY_LOC_MSG": "To be delivered here:",
        "COURIER_ACCEPT_ORDER_MSG": "Accept order?",
        "COURIER_ACCEPT_BTN": "✅ Accept",
        "ORDER_READY_MSG": lambda order_uuid: f"Order\n`{order_uuid}`\nis ready and handled to the courier.",
        "COUR_ORDER_IN_DELIVERY_MSG": lambda
            order_uuid: f"Please confirm receiving order\n`{order_uuid}`\n" \
                        f"by pressing button below.",
        "CUST_ORDER_IN_DELIVERY_MSG": lambda
            order_uuid: f"Order\n`{order_uuid}`\n" \
                        f"Status update:\nOrder is ready and handled to the courier.",
        "COUR_ORDER_IN_DELIVERY_BTN": "✅ Order received"
    },
    "de_DE": {
        "ASK_REGISTRATION_MSG": "This Telegram account isn't registered as a Restaurant account.\n"
                                "Please contact support for registration by replying to this message.\n"
                                "(By replying You agree Your contact info i.e. Telegram ID and Username "
                                "to be provided to Our Support Service.)",
        "WELCOME_MSG": f"Welcome to {BOT_NAME}-Restaurant!",
        "REG_REQUEST_MSG": lambda
            username,
            user_id,
            text: f"❗️ Incoming restaurant registration request\n" \
                  f"from @{username} (`{user_id}`):\n" \
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
        "DISH_AVAILABLE_SELECT_MSG": "Choose item to make it available.",
        "DISH_SET_AVAILABLE_MSG": "Selected item has been set available.",
        "DISH_UNAVAILABLE_SELECT_MSG": "Choose item to make it unavailable.",
        "DISH_SET_UNAVAILABLE_MSG": "Selected item has been set unavailable.",
        "DELETE_DISH_SELECT_MSG": "Select item to delete.",
        "DISH_DELETED_MSG": "Selected item has been deleted.",
        "DISH_ADDED_MSG": lambda dish_name: f"✅ Item: {dish_name} has been added to the Database.",
        "NO_DISH_NAME_MSG": "No item name was provided.",
        "EDIT_DISH_MSG": "Choose a item to edit",
        "GO_BACK_BTN": "⬅️ BACK",
        "EDIT_DISH_CHOSEN_MSG": lambda dish_name: f"Item to edit:\n{dish_name}",
        "EDIT_DISH_PARAM_MSG": "Which parameter of the item do You want to change?",
        "EDIT_DESC_BTN": "📝 Description",
        "EDIT_CAT_BTN": "🛍 Category",
        "EDIT_PRICE_BTN": "💶 Price",
        "EDIT_CATEGORY_MSG": lambda
            dish_uuid: f"Enter new category for the item:\n" \
                       f"Item UUID: {dish_uuid}",
        "CAT_SET_MSG": "✅ New category has been set for the item.",
        "EDIT_DESCRIPTION_MSG": lambda
            dish_uuid: f"Enter new description for the item:\n" \
                       f"Item UUID: {dish_uuid}",
        "DESC_SET_MSG": "✅ New description has been set for the item.",
        "EDIT_PRICE_MSG": lambda
            dish_uuid: f"Enter new price for the item:\n" \
                       f"Item UUID: {dish_uuid}",
        "PRICE_SET_MSG": "✅ New price has been set for the item.",
        "REST_ORDER_ACCEPTED_MSG": lambda order_uuid: f"✅ Accepted order\n`{order_uuid}`",
        "CUST_ORDER_ACCEPTED_MSG": lambda
            order_uuid: f"Order\n`{order_uuid}`\n" \
                        f"Status update:\n" \
                        f"Order received by the restaurant, looking for a courier.",
        "LOOKING_FOR_COURIER_MSG": lambda
            order_uuid,
            courier_fee,
            customer_name,
            customer_username,
            customer_phone,
            comment,
            rest_name,
            dishes,
            rest_address: f"New incoming order:\n`{order_uuid}`\n" \
                          f"Courier pay:\n€`{courier_fee}`\n" \
                          f"Customer's name:\n{customer_name}\n" \
                          f"Customer's Telegram:\n @{customer_username}\n" \
                          f"Customer's phone:\n{customer_phone}\n" \
                          f"Order comments:\n{comment}\n" \
                          f"Restaurant:\n`{rest_name}`\n" \
                          f"Item(s):\n{dishes}\n" \
                          f"Restaurant address:\n`{rest_address}`\n" \
                          f"Restaurant location:",
        "COURIER_DELIVERY_LOC_MSG": "To be delivered here:",
        "COURIER_ACCEPT_ORDER_MSG": "Accept order?",
        "COURIER_ACCEPT_BTN": "✅ Accept",
        "ORDER_READY_MSG": lambda order_uuid: f"Order\n`{order_uuid}`\nis ready and handled to the courier.",
        "COUR_ORDER_IN_DELIVERY_MSG": lambda
            order_uuid: f"Please confirm receiving order\n`{order_uuid}`\n" \
                        f"by pressing button below.",
        "CUST_ORDER_IN_DELIVERY_MSG": lambda
            order_uuid: f"Order\n`{order_uuid}`\n" \
                        f"Status update:\nOrder is ready and handled to the courier.",
        "COUR_ORDER_IN_DELIVERY_BTN": "✅ Order received"
    },
    "ru_RU": {
        "ASK_REGISTRATION_MSG": "Данный Телеграм аккаунт не зарегистрирован как заведение.\n"
                                "Пожалуйста, подайте заявку на регистрацию в Службу Поддержки путем ответа на это сообщение.\n"
                                "(Отвечая на данное сообщение Вы соглашаетесь на передачу ваших данных т.е. ника и ID Телеграм Нашей Службе Поддержки.)",
        "WELCOME_MSG": f"Добро пожаловать в {BOT_NAME}-Restaurant!",
        "REG_REQUEST_MSG": lambda
            username,
            user_id,
            text: f"❗️ Входящий запрос на регистрацию ресторана\n" \
                  f"от @{username} (`{user_id}`):\n" \
                  f"{text}",
        "REG_REQUEST_SENT_MSG": "Ваш запрос был отправлен Нашей Службе Поддержки.",
        "LANG_SEL_MENU": "Меню выбора языка",
        "CHANGE_LANG_MSG": "Выберите язык бота",
        "SEL_LANG_DE_BTN": "🇩🇪 Немецкий\n(Deutsch)",
        "SEL_LANG_EN_BTN": "🇺🇸 Английский\n(English)",
        "SEL_LANG_RU_BTN": "🇷🇺 Русский",
        "LANG_SELECTED_MSG": "Язык изменен на русский!",
        "OPEN_SHIFT_MSG": "Смена начата, теперь Вы будете получать заказы.",
        "CLOSE_SHIFT_MSG": "Смена закончена.",
        "DISH_AVAILABLE_SELECT_MSG": "Выберите товар, чтобы сделать его доступным для заказа.",
        "DISH_SET_AVAILABLE_MSG": "Выбранный товар теперь доступен для заказа.",
        "DISH_UNAVAILABLE_SELECT_MSG": "Выберите товар, чтобы сделать его недоступным для заказа.",
        "DISH_SET_UNAVAILABLE_MSG": "Выбранный товар теперь недоступен для заказа.",
        "DELETE_DISH_SELECT_MSG": "Выберите товар, чтобы удалить его.",
        "DISH_DELETED_MSG": "Выбранный товар был удален.",
        "DISH_ADDED_MSG": lambda dish_name: f"✅ Товар: {dish_name} был добавлен в базу данных.",
        "NO_DISH_NAME_MSG": "Наименование товара не найдено.",
        "EDIT_DISH_MSG": "Выберите товар для редактирования",
        "GO_BACK_BTN": "⬅️ НАЗАД",
        "EDIT_DISH_CHOSEN_MSG": lambda dish_name: f"Редактируемый товар:\n{dish_name}",
        "EDIT_DISH_PARAM_MSG": "Какой параметр Вы хотите изменить?",
        "EDIT_DESC_BTN": "📝 Описание",
        "EDIT_CAT_BTN": "🛍 Категория",
        "EDIT_PRICE_BTN": "💶 Цена",
        "EDIT_CATEGORY_MSG": lambda
            dish_uuid: f"Введите новую категорию:\n" \
                       f"UUID товара: {dish_uuid}",
        "CAT_SET_MSG": "✅ Товару присвоена новая категория.",
        "EDIT_DESCRIPTION_MSG": lambda
            dish_uuid: f"Введите новое описание товара:\n" \
                       f"UUID товара: {dish_uuid}",
        "DESC_SET_MSG": "✅ Товару присвоено новое описание.",
        "EDIT_PRICE_MSG": lambda
            dish_uuid: f"Введите новую цену товара:\n" \
                       f"UUID товара: {dish_uuid}",
        "PRICE_SET_MSG": "✅ Установлена новая цена для товара.",
        "REST_ORDER_ACCEPTED_MSG": lambda order_uuid: f"✅ Заказ принят\n`{order_uuid}`",
        "CUST_ORDER_ACCEPTED_MSG": lambda
            order_uuid: f"Заказ\n`{order_uuid}`\n" \
                        f"Новый статус:\n" \
                        f"Заказ принят заведением, ищем курьера.",
        "LOOKING_FOR_COURIER_MSG": lambda
            order_uuid,
            courier_fee,
            customer_name,
            customer_username,
            customer_phone,
            comment,
            rest_name,
            dishes,
            rest_address: f"Новый заказ:\n`{order_uuid}`\n" \
                          f"Вознаграждение курьера:\n€`{courier_fee}`\n" \
                          f"Имя покупателя:\n{customer_name}\n" \
                          f"Телеграм покупателя:\n @{customer_username}\n" \
                          f"Телефон покупателя:\n{customer_phone}\n" \
                          f"Комментарии:\n{comment}\n" \
                          f"Заведение:\n`{rest_name}`\n" \
                          f"Товар(ы):\n{dishes}\n" \
                          f"Адрес заведения:\n`{rest_address}`\n" \
                          f"Местоположение заведения:",
        "COURIER_DELIVERY_LOC_MSG": "Доставить сюда:",
        "COURIER_ACCEPT_ORDER_MSG": "Принять заказ?",
        "COURIER_ACCEPT_BTN": "✅ Принять",
        "ORDER_READY_MSG": lambda order_uuid: f"Заказ\n`{order_uuid}`\nготов и передан курьеру.",
        "COUR_ORDER_IN_DELIVERY_MSG": lambda
            order_uuid: f"Пожалуйста, подтвердите получение заказа\n`{order_uuid}`\n" \
                        f"нажатием кнопки.",
        "CUST_ORDER_IN_DELIVERY_MSG": lambda
            order_uuid: f"Заказ\n`{order_uuid}`\n" \
                        f"Новый статус:\nЗаказ готов и передан в доставку.",
        "COUR_ORDER_IN_DELIVERY_BTN": "✅ Заказ получен"
    }
}
