from environs import Env

env = Env()
env.read_env()

BOT_NAME = env.str("BRAND_NAME", default="LieferBot")

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
                  f"from `@{username}` (`{user_id}`):\n" \
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
        "COURIER_SUPPORT_MSG": "What's Your question?",
        "SUPPORT_FR_COUR_MSG": lambda
            customer_username,
            customer_id,
            req_text: f"❗️ New incoming support request from courier `@{customer_username}` " \
                      f"({customer_id}):\n{req_text}",
        "SUPPORT_SENT_MSG": "Your request was sent to our Support service.\nThey will contact you soon.",
        "COUR_ORDER_ACCEPTED_MSG": lambda order_uuid: f"✅ Order\n`{order_uuid}`\naccepted.",
        "COURIER_FOUND_MSG": lambda
            order_uuid,
            courier_name,
            courier_username,
            courier_phone: f"Order\n`{order_uuid}`\n" \
                           f"Status update:\nCourier found.\n" \
                           f"Courier's name:\n{courier_name}\n" \
                           f"Courier's Telegram:\n`@{courier_username}`\n" \
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
        "ASK_REG_MSG": "Dieses Telegram-Konto ist nicht als Kurierkonto registriert.\n"
                       "Bitte kontaktieren Sie den Support für die Registrierung, indem Sie auf diese Nachricht antworten.\n"
                       "(Mit Ihrer Antwort stimmen Sie zu, dass Ihre Kontaktinformationen, also Telegram-ID und Benutzername, unserem Support-Service zur Verfügung gestellt werden.)",
        "WELCOME_MSG": f"Willkommen bei {BOT_NAME}-Courier!",
        "REG_REQ_MSG": lambda
            username,
            user_id,
            text: f"❗️ Eingehende Kurieranmeldungsanfrage\n" \
                  f"von `@{username}` (`{user_id}`):\n{text}",
        "REG_REQ_SENT_MSG": "Ihre Anfrage wurde an unseren Support-Service gesendet.",
        "LANG_SEL_MENU": "Menü zur Auswahl der Bot-Sprache.",
        "CHANGE_LANG_MSG": "Wählen Sie die Bot-Sprache aus",
        "SEL_LANG_DE_BTN": "🇩🇪 Deutsch",
        "SEL_LANG_EN_BTN": "🇺🇸 Englisch\n(English)",
        "SEL_LANG_RU_BTN": "🇷🇺 Russisch\n(Русский)",
        "LANG_SELECTED_MSG": "Sprache gewechselt zu Deutsch!",
        "BALANCE_MSG": lambda salary: f"Ihr aktuelles Gehaltssaldo beträgt €{salary:.2f}",
        "CHANGE_TRANSPORT_MENU": "Bitte wählen Sie Ihren Transporttyp.",
        "FEET_BTN": "🚶‍➡️ Zu Fuß",
        "BICYCLE_BTN": "🚲 Fahrrad",
        "MOTORCYCLE_BTN": "🛵 Motorrad",
        "AUTO_BTN": "🚗 Auto",
        "TRANSPORT_SELECTED_MSG": "Transporttyp wurde ausgewählt.",
        "OPEN_SHIFT_MSG": "Schicht ist geöffnet, Sie können jetzt Bestellungen annehmen.",
        "CLOSE_SHIFT_MSG": "Schicht ist geschlossen.",
        "CANNOT_CLOSE_SHIFT_MSG": "Schicht kann wegen einer ungeschlossenen Bestellung nicht geschlossen werden.",
        "COURIER_SUPPORT_MSG": "Was ist Ihre Frage?",
        "SUPPORT_FR_COUR_MSG": lambda
            customer_username,
            customer_id,
            req_text: f"❗️ Neue eingehende Support-Anfrage von Kurier `@{customer_username}` " \
                      f"({customer_id}):\n{req_text}",
        "SUPPORT_SENT_MSG": "Ihre Anfrage wurde an unseren Support-Service gesendet.\nSie werden sich in Kürze mit Ihnen in Verbindung setzen.",
        "COUR_ORDER_ACCEPTED_MSG": lambda order_uuid: f"✅ Bestellung\n`{order_uuid}`\nakzeptiert.",
        "COURIER_FOUND_MSG": lambda
            order_uuid,
            courier_name,
            courier_username,
            courier_phone: f"Bestellung\n`{order_uuid}`\n" \
                           f"Statusaktualisierung:\nKurier gefunden.\n" \
                           f"Name des Kuriers:\n{courier_name}\n" \
                           f"Telegram des Kuriers:\n`@{courier_username}`\n" \
                           f"Telefon des Kuriers:\n{courier_phone}",
        "ORDER_ALREADY_ACCEPTED_MSG": "Entschuldigung, die Bestellung wurde bereits von einem anderen Kurier angenommen.",
        "REST_ORDER_READY_MSG": lambda
            order_uuid: f"Bitte drücken Sie den untenstehenden Knopf, wenn die Bestellung\n`{order_uuid}`\n" \
                        f"fertig und dem Kurier übergeben ist.",
        "REST_READY_BTN": "✅ Bestellung ist fertig",
        "COUR_IN_DELIVERY_MSG": lambda
            order_uuid: f"Bestellung\n`{order_uuid}`\n" \
                        f"ist in Zustellung.\n" \
                        f"Bitte drücken Sie den untenstehenden Knopf, wenn die Bestellung zugestellt ist.",
        "CUS_IN_DELIVERY_MSG": lambda
            order_uuid: f"Bestellung\n`{order_uuid}`\n" \
                        f"Statusaktualisierung:\nBestellung in Zustellung.",
        "DELIVERED_BTN": "✅ Bestellung zugestellt",
        "COUR_DELIVERED_MSG": lambda
            order_uuid: f"Bestellung\n`{order_uuid}`\n" \
                        f"ist zugestellt.\nVielen Dank :)",
        "CUS_DELIVERED_MSG": lambda
            order_uuid: f"Bestellung\n`{order_uuid}`\n" \
                        f"Statusaktualisierung:\n" \
                        f"Der Kurier hat gemeldet, dass Ihre Bestellung zugestellt wurde.\n" \
                        f"Bitte bestätigen Sie den Erhalt Ihrer Bestellung.",
        "ORDER_CLOSED_BTN": "✅ Bestellung erhalten"
    },
    "ru_RU": {
        "ASK_REG_MSG": "Этот профиль Телеграм не зарегистрирован как курьер.\n"
                       "Пожалуйста, свяжитесь со службой поддержки для регистрации путем ответа на это сообщение.\n"
                       "(Отвечая на это сообщение Вы соглашаетесь передать свои данные т.е. ник и ID Телеграм аккаунта Нашей Службе Поддержки.)",
        "WELCOME_MSG": f"Добро пожаловать в {BOT_NAME}-Courier",
        "REG_REQ_MSG": lambda
            username,
            user_id,
            text: f"❗️ Входящий запрос на регистрацию курьера\n" \
                  f"от `@{username}` (`{user_id}`):\n" \
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
        "COURIER_SUPPORT_MSG": "Задайте ваш вопрос:",
        "SUPPORT_FR_COUR_MSG": lambda
            customer_username,
            customer_id,
            req_text: f"❗️Новое входящие обращение от Курьера `@{customer_username}` " \
                      f"({customer_id}):\n{req_text}",
        "SUPPORT_SENT_MSG": "Ваше обращение было отправлено в службу поддержки.\nСкоро с Вами свяжутся.",
        "COUR_ORDER_ACCEPTED_MSG": lambda order_uuid: f"✅ Заказ\n`{order_uuid}`\nпринят.",
        "COURIER_FOUND_MSG": lambda
            order_uuid,
            courier_name,
            courier_username,
            courier_phone: f"Заказ\n`{order_uuid}`\n" \
                           f"Новый статус:\nКурьер найден.\n" \
                           f"Имя курьера:\n{courier_name}\n" \
                           f"Телеграм курьера:\n`@{courier_username}`\n" \
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
