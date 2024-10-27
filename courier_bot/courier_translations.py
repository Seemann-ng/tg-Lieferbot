from environs import Env

env = Env()
env.read_env()

BOT_NAME = env.str("BRAND_NAME")

texts = {
    "en_US": {
        "ASK_REG_MSG": "This Telegram account isn't registered as a Courier account.\n"
                       "Please contact support for registration by replying to this message.\n"
                       "(By replying You agree Your contact info i.e. Telegram ID and Username "
                       "to be provided to Our Support Service.)",
        "WELCOME_MSG": f"Welcome to {BOT_NAME}-Courier!",
        "REG_REQ_MSG": lambda
            username,
            user_id,
            text: f"❗️ Incoming courier registration request\n" \
                  f"from @{username} (`{user_id}`):\n" \
                  f"{text}",
        "REG_REQ_SENT_MSG": "Your request has been sent to Our Support Service.",
        "LANG_SEL_MENU": "Bot language selection menu.",
        "CHANGE_LANG_MSG": "Select bot language",
        "SEL_LANG_DE_BTN": "🇩🇪 German\n(Deutsch)",
        "SEL_LANG_EN_BTN": "🇺🇸 English",
        "SEL_LANG_RU_BTN": "🇷🇺 Russian\n(Русский)",
        "LANG_SELECTED_MSG": "Language changed to English!",
        "BALANCE_MSG": lambda salary: f"Your current salary balance is €{salary:.2f}",
        "CHANGE_TRANSPORT_MENU": "Please choose your transport type.",
        "FEET_BTN": "🚶‍➡️ On feet",
        "BICYCLE_BTN": "🚲 Bicycle",
        "MOTORCYCLE_BTN": "🛵 Motorcycle",
        "AUTO_BTN": "🚗 Automobile",
        "TRANSPORT_SELECTED_MSG": "Transport type has been selected.",
        "OPEN_SHIFT_MSG": "Shift is opened, now You can receive orders.",
        "CLOSE_SHIFT_MSG": "Shift is closed.",
        "CANNOT_CLOSE_SHIFT_MSG": "Can't close shift due to unclosed order.",
        "COUR_ORDER_ACCEPTED_MSG": lambda order_uuid: f"✅ Order\n`{order_uuid}`\naccepted.",
        "COURIER_FOUND_MSG": lambda
            order_uuid,
            courier_name,
            courier_username,
            courier_phone: f"Order\n`{order_uuid}`\n" \
                           f"Status update:\nCourier found.\n" \
                           f"Courier's name:\n{courier_name}\n" \
                           f"Courier's Telegram:\n@{courier_username}\n" \
                           f"Courier's phone:\n{courier_phone}",
        "ORDER_ALREADY_ACCEPTED_MSG": "Sorry, order is already accepted by another courier.",
        "REST_ORDER_READY_MSG": lambda
            order_uuid: f"Please, press the button below when order\n`{order_uuid}`\n" \
                        f"is ready and handled to the courier.",
        "REST_READY_BTN": "✅ Order is ready",
        "COUR_IN_DELIVERY_MSG": lambda
            order_uuid: f"Order\n`{order_uuid}`\n" \
                        f"is in delivery.\n" \
                        f"Please press the button below when order is delivered.",
        "CUS_IN_DELIVERY_MSG": lambda
            order_uuid: f"Order\n`{order_uuid}`\n" \
                        f"Status update:\nOrder in delivery.",
        "DELIVERED_BTN": "✅ Order delivered",
        "COUR_DELIVERED_MSG": lambda
            order_uuid: f"Order\n`{order_uuid}`\n" f"is delivered.\n" \
                        f"Thank You:)",
        "CUS_DELIVERED_MSG": lambda
            order_uuid: f"Order\n`{order_uuid}`\n" \
                        f"Status update:\nCourier reported Your order as delivered.\n" \
                        f"Please confirm receiving Your order.",
        "ORDER_CLOSED_BTN": "✅ Order received"
    },
    "de_DE": {
        "ASK_REG_MSG": "This Telegram account isn't registered as a Courier account.\n"
                       "Please contact support for registration by replying to this message.\n"
                       "(By replying You agree Your contact info i.e. Telegram ID and Username "
                       "to be provided to Our Support Service.)",
        "WELCOME_MSG": f"Welcome to {BOT_NAME}-Courier!",
        "REG_REQ_MSG": lambda
            username,
            user_id,
            text: f"❗️ Incoming courier registration request\n" \
                  f"from @{username} (`{user_id}`):\n" \
                  f"{text}",
        "REG_REQ_SENT_MSG": "Your request has been sent to Our Support Service.",
        "LANG_SEL_MENU": "Bot language selection menu.",
        "CHANGE_LANG_MSG": "Select bot language",
        "SEL_LANG_DE_BTN": "🇩🇪 German\n(Deutsch)",
        "SEL_LANG_EN_BTN": "🇺🇸 English",
        "SEL_LANG_RU_BTN": "🇷🇺 Russian\n(Русский)",
        "LANG_SELECTED_MSG": "Language changed to English!",
        "BALANCE_MSG": lambda salary: f"Your current salary balance is €{salary:.2f}",
        "CHANGE_TRANSPORT_MENU": "Please choose your transport type.",
        "FEET_BTN": "🚶‍➡️ On feet",
        "BICYCLE_BTN": "🚲 Bicycle",
        "MOTORCYCLE_BTN": "🛵 Motorcycle",
        "AUTO_BTN": "🚗 Automobile",
        "TRANSPORT_SELECTED_MSG": "Transport type has been selected.",
        "OPEN_SHIFT_MSG": "Shift is opened, now You can receive orders.",
        "CLOSE_SHIFT_MSG": "Shift is closed.",
        "CANNOT_CLOSE_SHIFT_MSG": "Can't close shift due to unclosed order.",
        "COUR_ORDER_ACCEPTED_MSG": lambda order_uuid: f"✅ Order\n`{order_uuid}`\naccepted.",
        "COURIER_FOUND_MSG": lambda
            order_uuid,
            courier_name,
            courier_username,
            courier_phone: f"Order\n`{order_uuid}`\n" \
                           f"Status update:\nCourier found.\n" \
                           f"Courier's name:\n{courier_name}\n" \
                           f"Courier's Telegram:\n@{courier_username}\n" \
                           f"Courier's phone:\n{courier_phone}",
        "ORDER_ALREADY_ACCEPTED_MSG": "Sorry, order is already accepted by another courier.",
        "REST_ORDER_READY_MSG": lambda
            order_uuid: f"Please, press the button below when order\n`{order_uuid}`\n" \
                        f"is ready and handled to the courier.",
        "REST_READY_BTN": "✅ Order is ready",
        "COUR_IN_DELIVERY_MSG": lambda
            order_uuid: f"Order\n`{order_uuid}`\n" \
                        f"is in delivery.\n" \
                        f"Please press the button below when order is delivered.",
        "CUS_IN_DELIVERY_MSG": lambda
            order_uuid: f"Order\n`{order_uuid}`\n" \
                        f"Status update:\nOrder in delivery.",
        "DELIVERED_BTN": "✅ Order delivered",
        "COUR_DELIVERED_MSG": lambda
            order_uuid: f"Order\n`{order_uuid}`\n" f"is delivered.\n" \
                        f"Thank You:)",
        "CUS_DELIVERED_MSG": lambda
            order_uuid: f"Order\n`{order_uuid}`\n" \
                        f"Status update:\nCourier reported Your order as delivered.\n" \
                        f"Please confirm receiving Your order.",
        "ORDER_CLOSED_BTN": "✅ Order received"
    },
    "ru_RU": {
        "ASK_REG_MSG": "Этот профиль Телеграм не зарегестрирован как курьер.\n"
                       "Пожалуйста, свяжитесь со службой поддержки для регистрации путем ответа на это сообщение.\n"
                       "(Отвечая на это сообщение Вы соглашаетесь передать свои данные т.е. юзернейм и ID Телеграм аккаунта Нашей Службе Поддержки.)",
        "WELCOME_MSG": f"Добро пожаловать в {BOT_NAME}-Courier",
        "REG_REQ_MSG": lambda
            username,
            user_id,
            text: f"❗️ Входящий запрос на регистрацию курьера\n" \
                  f"от @{username} (`{user_id}`):\n" \
                  f"{text}",
        "REG_REQ_SENT_MSG": "Ваш запрос был отправлен в Нашу Службу Поддержки.",
        "LANG_SEL_MENU": "Меню выбора языка",
        "CHANGE_LANG_MSG": "Выберите язык бота",
        "SEL_LANG_DE_BTN": "🇩🇪 Немецкий\n(Deutsch)",
        "SEL_LANG_EN_BTN": "🇺🇸 Английский\n(English)",
        "SEL_LANG_RU_BTN": "🇷🇺 Русский",
        "LANG_SELECTED_MSG": "Язык изменен на русский!",
        "BALANCE_MSG": lambda salary: f"Ваш текущий зарплатный баланс €{salary:.2f}",
        "CHANGE_TRANSPORT_MENU": "Пожалуйста, выберите Ваш тип транспорта.",
        "FEET_BTN": "🚶‍➡️ Пешком",
        "BICYCLE_BTN": "🚲 Велосипед",
        "MOTORCYCLE_BTN": "🛵 Мотоцикл",
        "AUTO_BTN": "🚗 Автомобиль",
        "TRANSPORT_SELECTED_MSG": "Тип транспорта выбран.",
        "OPEN_SHIFT_MSG": "Смена начата, теперь Вы будете получать заказы.",
        "CLOSE_SHIFT_MSG": "Смена закончена.",
        "CANNOT_CLOSE_SHIFT_MSG": "Не удалось закончить смену из-за незакрытого заказа.",
        "COUR_ORDER_ACCEPTED_MSG": lambda order_uuid: f"✅ Заказ\n`{order_uuid}`\nпринят.",
        "COURIER_FOUND_MSG": lambda
            order_uuid,
            courier_name,
            courier_username,
            courier_phone: f"Заказ\n`{order_uuid}`\n" \
                           f"Новый статус:\nКурьер найден.\n" \
                           f"Имя курьера:\n{courier_name}\n" \
                           f"Телеграм курьера:\n@{courier_username}\n" \
                           f"Номер телефона курьера:\n{courier_phone}",
        "ORDER_ALREADY_ACCEPTED_MSG": "Упс, этот заказ уже принял другой курьер.",
        "REST_ORDER_READY_MSG": lambda
            order_uuid: f"Пожалуйста нажмите кнопку, когда заказ\n`{order_uuid}`\n" \
                        f"будет готов и передан курьеру.",
        "REST_READY_BTN": "✅ Заказ готов",
        "COUR_IN_DELIVERY_MSG": lambda
            order_uuid: f"Заказ\n`{order_uuid}`\n" \
                        f"принят в доставку.\n" \
                        f"Пожалуйста, нажмите кнопку, когда заказ будет доставлен.",
        "CUS_IN_DELIVERY_MSG": lambda
            order_uuid: f"Заказ\n`{order_uuid}`\n" \
                        f"Новый статус:\nЗаказ принят в доставку.",
        "DELIVERED_BTN": "✅ Заказ доставлен",
        "COUR_DELIVERED_MSG": lambda
            order_uuid: f"Заказ\n`{order_uuid}`\nдоставлен.\n" \
                        f"Спасибо :)",
        "CUS_DELIVERED_MSG": lambda
            order_uuid: f"Заказ\n`{order_uuid}`\n" \
                        f"Новый статус:\nКурьер отметил Ваш заказ как доставленный.\n" \
                        f"Пожалуйста, подтвердите получение нажав на кнопку.",
        "ORDER_CLOSED_BTN": "✅ Заказ доставлен"
    }
}
