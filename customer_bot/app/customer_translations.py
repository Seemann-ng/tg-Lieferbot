from environs import Env

env = Env()
env.read_env()

BOT_NAME = env.str("BRAND_NAME")

texts = {
    "en_US": {
        # Localization variables.
        "AGREEMENT_MENU_PLACEHOLDER": "📑 Agreement",
        # Menu buttons.
        "SHOW_AGREEMENT_BTN": "🔍📑 Show Customer Agreement",
        "ACCEPT_AGREEMENT_BTN": "📝 Accept Customer Agreement",
        "REG_PHONE_MENU_PLACEHOLDER": "📱 Phone number input",
        "REG_PHONE_MAN_BTN": "👨🏼‍💻 Input phone number manually",
        "REG_PHONE_IMPORT_BTN": "⬆️ Import phone number from account",
        "REG_LOCATION_BTN": "🌍 Send location",
        "REG_LOCATION_PLACEHOLDER": "🌍 Location",
        "MAIN_MENU_BTN": "🟰 Main Menu",
        "NEW_ORDER_BTN": "⭕️ New Order",
        "MY_ORDERS_BTN": "📑 My Orders",
        "OPTIONS_BTN": "🟰 Options",
        "CHANGE_LANG_BTN": "💬 Change language",
        "SEL_LANG_DE_BTN": "🇩🇪 German\n(Deutsch)",
        "SEL_LANG_EN_BTN": "🇺🇸 English",
        "SEL_LANG_RU_BTN": "🇷🇺 Russian\n(Русский)",
        "CONTACT_SUPPORT_BTN": "📞 Contact support",
        "RESET_CONTACT_INFO_BTN": "⚠️ Reset Contact Info",
        "CONFIRM_RESET_BTN": "✅ YES, reset my contact info",
        "DELETE_PROFILE_BTN": "⚠️ Delete profile",
        "CONFIRM_DELETE_PROFILE_BTN": "✅ YES, delete my profile",
        "CONFIRM_LOCATION_BTN": "✅ Yes!",
        "WRONG_LOCATION_BTN": "❌ No.",
        "GO_BACK_BTN": "⬅️ Go back",
        "CART_BTN": "🛒 My cart",
        "CANCEL_ORDER_BTN": "🚫 CANCEL ORDER",
        "ADD_DISH_BTN": "✅ Add to cart",
        "MAKE_ORDER_BTN": "💳 Confirm order",
        "ADD_COMMENT_BTN": "📄 Add order comment",
        "ADD_MORE_BTN": "🛍 Continue shopping",
        "DELETE_ITEM_BTN": "📤 Delete item",
        "PAID_BTN": "✅ I have paid",
        "IN_DEV": "I've told You, IT IS IN DEVELOPMENT!",
        # Bot messages.
        "WELCOME_BACK_MSG": lambda customer_name: f"Welcome back, {customer_name}!",
        "MAIN_MENU_MSG": "You're in main menu now.",
        "FIRST_WELCOME_MSG": f"Welcome to the {BOT_NAME}.",
        "ASK_AGREEMENT_MSG": "To proceed, You have to accept our Customer Agreement.",
        "AGREEMENT_TEXT": "SAMPLE AGREEMENT TEXT.",
        "AGREEMENT_ACCEPTED_MSG": "✅ Customer Agreement was accepted.",
        "REG_NAME_MSG": "How can I call You?",
        "REG_NAME_PLACEHOLDER": "Your name",
        "REG_NAME_RECEIVED_MSG": lambda new_name: f"Your name has been changed to: {new_name}.",
        "REG_PHONE_METHOD_MSG": "How would You like to provide your phone number?",
        "REG_PHONE_MSG": "Please provide us Your phone number (without '+'!).",
        "REG_PHONE_PLACEHOLDER": "Your phone number",
        "PHONE_RECEIVED_MSG": lambda phone_number: f"Your phone number has been changed to: {phone_number}.",
        "INVALID_PHONE_MSG": "‼️ Invalid phone number.",
        "REG_LOCATION_MSG": "Please send Your location.",
        "REG_LOCATION_RECEIVED_MSG": "Your current location is:",
        "NO_ORDERS_FOUND_MSG": "😞 No orders were found.",
        "OPTIONS_MSG": "Here You can contact Support, reset or delete Your contact info.",
        "CUS_SUPPORT_MSG": "What's Your question?",
        "SUPPORT_FR_CUS_MSG": lambda
            customer_username,
            customer_id,
            req_text: f"❗️ New incoming support request from customer @{customer_username}" \
                      f"({customer_id}):\n{req_text}",
        "SUPPORT_SENT_MSG": "Your request was sent to our Support service.\nThey will contact you soon.",
        "LANG_SEL_MENU": "Bot language selection menu.",
        "CHANGE_LANG_MSG": "Select bot language",
        "RESET_CONTACT_INFO_MSG": "⚠️ Are You sure You want to reset Your contact info?",
        "CONTACT_INFO_DELETED_MSG": " ⚠️Your contact info were deleted.",
        "DELETE_PROFILE_MSG": "⚠️ Are You sure You want to delete Your profile?",
        "PROFILE_DELETED_MSG": "⚠️ Your profile has been deleted.",
        "EXITING_ORDER_MENU_MSG": "Going back to main menu.",
        "DELETING_CART_ALERT": "⚠️ Your cart was cleared.",
        "GOING_BACK_MSG": "Going back...",
        "NO_COURIERS_MSG": "No couriers available at the moment, please try again later.",
        "LOCATION_NOT_FOUND_MSG": "Contact information wasn't found.\n"
                                  "Please, reset Your contact information.",
        "CONFIRM_LOCATION_MSG": "Is this delivery address right?",
        "CHOOSE_REST_TYPE_MSG": "Please, choose a restaurant type.",
        "REST_TYPE_SELECTED_MSG": lambda
            rest_type: f"Selected restaurant type:\n" \
                       f"{rest_type}",
        "CHOOSE_REST_MSG": "Please, choose a restaurant.",
        "REST_SELECTED_MSG": lambda
            restaurant: f"Selected restaurant:\n" \
                        f"{restaurant}",
        "CHOOSE_DISH_CATEGORY_MSG": "Please, choose an item category.",
        "DISH_CAT_SELECTED_MSG": lambda
            dish_cat: f"Selected item category:\n" \
                      f"{dish_cat}",
        "CHOOSE_DISH_MSG": "Please, choose Your item",
        "DISH_SELECTED_MSG": lambda
            dish: f"Selected item:\n" \
                  f"{dish[0]}\n" \
                  f"Description:\n" \
                  f"{dish[1]}\n" \
                  f"Price:\n" \
                  f"€{dish[2]}",
        "ADD_DISH_MSG": "Add item to the cart?",
        "YOUR_CART_MSG": lambda
            dishes,
            subtotal,
            courier_fee,
            service_fee,
            total: f"🛒 Your cart:\n" \
                   f"{dishes}\n" \
                   f"Subtotal:\n" \
                   f"€{subtotal}\n" \
                   f"Courier fee:\n" \
                   f"€{courier_fee}\n" \
                   f"Service fee:\n" \
                   f"€{service_fee}\n" \
                   f"----\n" \
                   f"Total:\n" \
                   f"€{total}",
        "CART_ACTIONS_MSG": "Actions:",
        "DELETE_ITEM_MSG": "Choose item to delete",
        "MY_ORDERS_MSG": lambda
            orders,
            status: f"Order Number:\n`{orders[0][0]}`\n" \
                    f"from: {orders[0][1]}\n" \
                    f"Courier: {orders[0][2]}\n" \
                    f"Item(s): {orders[0][3]}\n" \
                    f"Total: €{orders[0][4]}\n" \
                    f"Date: {orders[0][5]}\n" \
                    f"Status: {status}\n" \
                    f"Order closed:{orders[0][7]}",
        "STATUS_CODES": {
            "-1": "Cancelled",
            "0": "Closed",
            "1": "Created",
            "2": "Paid",
            "3": "Accepted by the Restaurant, looking for a Courier",
            "4": "Preparing, Courier found",
            "5": "Ready, handled over to a Courier",
            "6": "In delivery",
            "7": "Delivered"
        },
        "ADD_COMMENT_MSG": "Add comment for Your order:",
        "COMMENT_ADDED_MSG": "Your comment was added.",
        "TO_CART_MSG": "Proceed to cart?",
        "ORDER_CREATED_MSG": lambda
            order_info: f"Order created:\n`{order_info[0]}`\n" \
                        f"Restaurant:\n{order_info[3]}\n" \
                        f"Item(s):\n{order_info[7]}\n" \
                        f"Total:\n€`{order_info[11]}`\n" \
                        f"Date:\n{order_info[12]}\n" \
                        f"Comments:\n{order_info[14]}",
        "PAYMENT_MENU_MSG": lambda url: f"Please proceed to payment via this link: {url}",
        "PAYPAL_ORDER_CREATION_FAIL_MSG": "Something went wrong while generating payment link, please, try again later.",
        "CUS_PAYMENT_CONFIRMED_MSG": lambda
            order_uuid: f"Payment for order\n" \
                        f"`{order_uuid}`\n" \
                        f"confirmed",
        "REST_ACCEPT_ORDER_BTN": "✅ Accept order",
        "WAIT_FOR_CONFIRMATION_MSG": lambda
            order_uuid: f"Payment confirmation from the Service has not been obtained\n" \
                        f"Order №\n`{order_uuid}`.",
        "ORDER_CLOSED_MSG": lambda order_uuid: f"Order closed:\n`{order_uuid}`",
        "CANCEL_MSG": lambda order_uuid: f"Order cancelled\n`{order_uuid}`",
        "REST_NEW_ORDER_MSG": lambda
            order_uuid,
            dishes,
            subtotal,
            comment: f"New incoming order\n" \
                     f"`{order_uuid}`\n" \
                     f"Item(s):\n" \
                     f"{dishes}\n" \
                     f"To be paid:\n" \
                     f"`{subtotal}`\n" \
                     f"Comments:\n" \
                     f"{comment}"
    },
    "de_DE": {
        # Localization variables.
        "AGREEMENT_MENU_PLACEHOLDER": "📑 Vereinbarung",
        # Menu buttons.
        "SHOW_AGREEMENT_BTN": "🔍📑 Kundevereinbarung anzeigen",
        "ACCEPT_AGREEMENT_BTN": "📝 Kundevereinbarung akzeptieren",
        "REG_PHONE_MENU_PLACEHOLDER": "📱 Telefonnummer eingeben",
        "REG_PHONE_MAN_BTN": "👨🏼‍💻 Telefonnummer manuell eingeben",
        "REG_PHONE_IMPORT_BTN": "⬆️ Telefonnummer vom Konto importieren",
        "REG_LOCATION_BTN": "🌍 Standort senden",
        "REG_LOCATION_PLACEHOLDER": "🌍 Standort",
        "MAIN_MENU_BTN": "🟰 Hauptmenü",
        "NEW_ORDER_BTN": "⭕️ Neue Bestellung",
        "MY_ORDERS_BTN": "📑 Meine Bestellungen",
        "OPTIONS_BTN": "🟰 Optionen",
        "CHANGE_LANG_BTN": "💬 Sprache ändern",
        "SEL_LANG_DE_BTN": "🇩🇪 Deutsch",
        "SEL_LANG_EN_BTN": "🇺🇸 Englisch\n(English)",
        "SEL_LANG_RU_BTN": "🇷🇺 Russisch\n(Русский)",
        "CONTACT_SUPPORT_BTN": "📞 Support kontaktieren",
        "RESET_CONTACT_INFO_BTN": "⚠️ Kontaktinformationen zurücksetzen",
        "CONFIRM_RESET_BTN": "✅ JA, meine Kontaktinformationen zurücksetzen",
        "DELETE_PROFILE_BTN": "⚠️ Profil löschen",
        "CONFIRM_DELETE_PROFILE_BTN": "✅ JA, mein Profil löschen",
        "CONFIRM_LOCATION_BTN": "✅ Ja!",
        "WRONG_LOCATION_BTN": "❌ Nein.",
        "GO_BACK_BTN": "⬅️ Zurück",
        "CART_BTN": "🛒 Mein Warenkorb",
        "CANCEL_ORDER_BTN": "🚫 BESTELLUNG STORNIEREN",
        "ADD_DISH_BTN": "✅ Zum Warenkorb hinzufügen",
        "MAKE_ORDER_BTN": "💳 Bestellung bestätigen",
        "ADD_COMMENT_BTN": "📄 Kommentar zur Bestellung hinzufügen",
        "ADD_MORE_BTN": "🛍 Weiter einkaufen",
        "DELETE_ITEM_BTN": "📤 Artikel löschen",
        "PAID_BTN": "✅ Ich habe bezahlt.",
        "IN_DEV": "Ich habe es Ihnen gesagt, ES IST IN ENTWICKLUNG!",
        # Bot messages.
        "WELCOME_BACK_MSG": lambda customer_name: f"Willkommen zurück, {customer_name}!",
        "MAIN_MENU_MSG": "Sie befinden sich jetzt im Hauptmenü.",
        "FIRST_WELCOME_MSG": f"Willkommen bei {BOT_NAME}.",
        "ASK_AGREEMENT_MSG": "Um fortzufahren, müssen Sie unsere Kundenvereinbarung akzeptieren.",
        "AGREEMENT_TEXT": "BEISPIELTEXT DER VEREINBARUNG.",
        "AGREEMENT_ACCEPTED_MSG": "✅ Die Kundenvereinbarung wurde akzeptiert.",
        "REG_NAME_MSG": "Wie kann ich Sie ansprechen?",
        "REG_NAME_PLACEHOLDER": "Ihr Name",
        "REG_NAME_RECEIVED_MSG": lambda new_name: f"Ihr Name wurde geändert zu: {new_name}.",
        "REG_PHONE_METHOD_MSG": "Wie möchten Sie Ihre Telefonnummer angeben?",
        "REG_PHONE_MSG": "Bitte geben Sie uns Ihre Telefonnummer an (ohne '+'!).",
        "REG_PHONE_PLACEHOLDER": "Ihre Telefonnummer",
        "PHONE_RECEIVED_MSG": lambda phone_number: f"Ihre Telefonnummer wurde geändert zu: {phone_number}.",
        "INVALID_PHONE_MSG": "‼️ Ungültige Telefonnummer.",
        "REG_LOCATION_MSG": "Bitte senden Sie Ihren Standort.",
        "REG_LOCATION_RECEIVED_MSG": "Ihr aktueller Standort ist:",
        "NO_ORDERS_FOUND_MSG": "😞 Es wurden keine Bestellungen gefunden.",
        "OPTIONS_MSG": "Hier können Sie den Support kontaktieren, Ihre Kontaktinformationen zurücksetzen oder löschen.",
        "CUS_SUPPORT_MSG": "Was ist Ihre Frage?",
        "SUPPORT_FR_CUS_MSG": lambda
            customer_username,
            customer_id,
            req_text: f"❗️ Neue eingehende Support-Anfrage von Kunde @{customer_username} " \
                      f"({customer_id}):\n{req_text}",
        "SUPPORT_SENT_MSG": "Ihre Anfrage wurde an unseren Support-Service gesendet.\nSie werden sich in Kürze mit Ihnen in Verbindung setzen.",
        "LANG_SEL_MENU": "Sprachauswahlmenü des Bots.",
        "CHANGE_LANG_MSG": "Wählen Sie die Sprache des Bots",
        "RESET_CONTACT_INFO_MSG": "⚠️ Sind Sie sicher, dass Sie Ihre Kontaktinformationen zurücksetzen möchten?",
        "CONTACT_INFO_DELETED_MSG": "⚠️ Ihre Kontaktinformationen wurden gelöscht.",
        "DELETE_PROFILE_MSG": "⚠️ Sind Sie sicher, dass Sie Ihr Profil löschen möchten?",
        "PROFILE_DELETED_MSG": "⚠️ Ihr Profil wurde gelöscht.",
        "EXITING_ORDER_MENU_MSG": "Zurück zum Hauptmenü.",
        "DELETING_CART_ALERT": "⚠️ Ihr Warenkorb wurde geleert.",
        "GOING_BACK_MSG": "Zurückgehen...",
        "NO_COURIERS_MSG": "Derzeit sind keine Kuriere verfügbar, bitte versuchen Sie es später noch einmal.",
        "LOCATION_NOT_FOUND_MSG": "Kontaktinformationen wurden nicht gefunden.\nBitte setzen Sie Ihre Kontaktinformationen zurück.",
        "CONFIRM_LOCATION_MSG": "Ist diese Lieferadresse korrekt?",
        "CHOOSE_REST_TYPE_MSG": "Bitte wählen Sie eine Art von Restaurant.",
        "REST_TYPE_SELECTED_MSG": lambda rest_type: f"Ausgewählte Restaurantart:\n{rest_type}",
        "CHOOSE_REST_MSG": "Bitte wählen Sie ein Restaurant.",
        "REST_SELECTED_MSG": lambda restaurant: f"Ausgewähltes Restaurant:\n{restaurant}",
        "CHOOSE_DISH_CATEGORY_MSG": "Bitte wählen Sie eine Kategorie.",
        "DISH_CAT_SELECTED_MSG": lambda dish_cat: f"Ausgewählte Kategorie:\n{dish_cat}",
        "CHOOSE_DISH_MSG": "Bitte wählen Sie Ihren Artikel",
        "DISH_SELECTED_MSG": lambda
            dish: f"Ausgewählter Artikel:\n{dish[0]}" \
                  f"\nBeschreibung:\n{dish[1]}"\
                  f"\nPreis:\n€{dish[2]}",
        "ADD_DISH_MSG": "Möchten Sie den Artikel in den Warenkorb legen?",
        "YOUR_CART_MSG": lambda
            dishes,
            subtotal,
            courier_fee,
            service_fee,
            total: f"🛒 Ihr Warenkorb:\n{dishes}\n" \
                   f"Zwischensumme:\n€{subtotal}\n" \
                   f"Kuriergeühr:\n€{courier_fee}\n" \
                   f"Servicegebühr:\n€{service_fee}\n" \
                   f"----\nGesamt:\n€{total}",
        "CART_ACTIONS_MSG": "Aktionen:",
        "DELETE_ITEM_MSG": "Artikel zum Löschen auswählen",
        "MY_ORDERS_MSG": lambda
            orders,
            status: f"Bestellnummer:\n`{orders[0][0]}`\n" \
                    f"Von: {orders[0][1]}\n" \
                    f"Kurier: {orders[0][2]}\n" \
                    f"Artikel: {orders[0][3]}\n" \
                    f"Gesamt: €{orders[0][4]}\n" \
                    f"Datum: {orders[0][5]}\n" \
                    f"Status: {status}\n" \
                    f"Bestellung geschlossen: {orders[0][7]}",
        "STATUS_CODES": {
            "-1": "Storniert",
            "0": "Geschlossen",
            "1": "Erstellt",
            "2": "Bezahlt",
            "3": "Vom Restaurant akzeptiert, auf Kurier wird gewartet",
            "4": "In Vorbereitung, Kurier gefunden",
            "5": "Fertig, an den Kurier übergeben",
            "6": "In Zustellung",
            "7": "Geliefert"
        },
        "ADD_COMMENT_MSG": "Kommentar zu Ihrer Bestellung hinzufügen:",
        "COMMENT_ADDED_MSG": "Ihr Kommentar wurde hinzugefügt.",
        "TO_CART_MSG": "Zum Warenkorb gehen?",
        "ORDER_CREATED_MSG": lambda
            order_info: f"Bestellung erstellt:\n`{order_info[0]}`\n" \
                        f"Restaurant:\n{order_info[3]}\n" \
                        f"Artikel:\n{order_info[7]}\n" \
                        f"Gesamt:\n€`{order_info[11]}`\n" \
                        f"Datum:\n{order_info[12]}\n" \
                        f"Kommentare:\n{order_info[14]}",
        "PAYMENT_MENU_MSG": lambda url: f"Bitte führen Sie die Zahlung über diesen Link aus: {url}",
        "PAYPAL_ORDER_CREATION_FAIL_MSG": "Es ist ein Fehler beim Generieren des Zahlungslinks aufgetreten, bitte versuchen Sie es später erneut.",
        "CUS_PAYMENT_CONFIRMED_MSG": lambda order_uuid: f"Zahlung für Bestellung\n`{order_uuid}`\nbestätigt",
        "REST_ACCEPT_ORDER_BTN": "✅ Bestellung akzeptieren",
        "WAIT_FOR_CONFIRMATION_MSG": lambda order_uuid: f"Zahlungsbestätigung vom Service wurde nicht erhalten\nBestellung №\n`{order_uuid}`.",
        "ORDER_CLOSED_MSG": lambda order_uuid: f"Bestellung geschlossen:\n`{order_uuid}`",
        "CANCEL_MSG": lambda order_uuid: f"Bestellung storniert\n`{order_uuid}`",
        "REST_NEW_ORDER_MSG": lambda
            order_uuid,
            dishes,
            subtotal,
            comment: f"Neue eingehende Bestellung\n`{order_uuid}`\n" \
                     f"Artikel:\n{dishes}\n" \
                     f"Zu zahlen:\n`{subtotal}`\n" \
                     f"Kommentare:\n{comment}"
    },
    "ru_RU": {
        # Localization variables.
        "AGREEMENT_MENU_PLACEHOLDER": "📑 Пользовательское Соглашение",
        # Menu buttons.
        "SHOW_AGREEMENT_BTN": "🔍📑 Показать Соглашение",
        "ACCEPT_AGREEMENT_BTN": "📝 Принять Соглашение",
        "REG_PHONE_MENU_PLACEHOLDER": "📱 Ввод номера телефона",
        "REG_PHONE_MAN_BTN": "👨🏼‍💻 Ввести номер вручную",
        "REG_PHONE_IMPORT_BTN": "⬆️ Импортировать номер из профиля",
        "REG_LOCATION_BTN": "🌍 Отправить местоположение",
        "REG_LOCATION_PLACEHOLDER": "🌍 Местоположение",
        "MAIN_MENU_BTN": "🟰 Главное меню",
        "NEW_ORDER_BTN": "⭕️ Новый заказ",
        "MY_ORDERS_BTN": "📑 Мои заказы",
        "OPTIONS_BTN": "🟰 Опции",
        "CHANGE_LANG_BTN": "💬 Выбор языка",
        "SEL_LANG_DE_BTN": "🇩🇪 Немецкий\n(Deutsch)",
        "SEL_LANG_EN_BTN": "🇺🇸 Английский\n(English)",
        "SEL_LANG_RU_BTN": "🇷🇺 Русский",
        "CONTACT_SUPPORT_BTN": "📞 Служба поддержки",
        "RESET_CONTACT_INFO_BTN": "⚠️ Сбросить контактные данные",
        "CONFIRM_RESET_BTN": "✅ ДА, сбросить контактные данные",
        "DELETE_PROFILE_BTN": "⚠️ Удалить профиль",
        "CONFIRM_DELETE_PROFILE_BTN": "✅ ДА, удалить мой профиль",
        "CONFIRM_LOCATION_BTN": "✅ Да!",
        "WRONG_LOCATION_BTN": "❌ Нет.",
        "GO_BACK_BTN": "⬅️ Назад",
        "CART_BTN": "🛒 Моя корзина",
        "CANCEL_ORDER_BTN": "🚫 ОТМЕНИТЬ ЗАКАЗ",
        "ADD_DISH_BTN": "✅ Добавить в корзину",
        "MAKE_ORDER_BTN": "💳 Подтвердить заказ",
        "ADD_COMMENT_BTN": "📄 Добавить комментарий",
        "ADD_MORE_BTN": "🛍 Продолжить покупки",
        "DELETE_ITEM_BTN": "📤 Удалить товар",
        "PAID_BTN": "✅ Я оплатил",
        "IN_DEV": "Раздел в разработке",
        # Bot messages.
        "WELCOME_BACK_MSG": lambda customer_name: f"Здравствуйте, {customer_name}!",
        "MAIN_MENU_MSG": "Вы в главном меню.",
        "FIRST_WELCOME_MSG": f"Добро пожаловать в {BOT_NAME}.",
        "ASK_AGREEMENT_MSG": "Для продолжения Вам необходимо принять наше Пользовательское Соглашение.",
        "AGREEMENT_TEXT": "SAMPLE AGREEMENT TEXT.",
        "AGREEMENT_ACCEPTED_MSG": "✅ Пользовательское Соглашение принято.",
        "REG_NAME_MSG": "Как я могу к Вам обращаться?",
        "REG_NAME_PLACEHOLDER": "Ваше имя",
        "REG_NAME_RECEIVED_MSG": lambda new_name: f"Ваше имя изменено на: {new_name}.",
        "REG_PHONE_METHOD_MSG": "Как Вы хотите ввести Ваш номер телефона?",
        "REG_PHONE_MSG": "Пожалуйста, введите Ваш номер телефона (без '+'!).",
        "REG_PHONE_PLACEHOLDER": "Ваш номер телефона",
        "PHONE_RECEIVED_MSG": lambda phone_number: f"Ваш номер телефона изменен на: {phone_number}.",
        "INVALID_PHONE_MSG": "‼️ Некорректный номер телефона.",
        "REG_LOCATION_MSG": "Пожалуйста, отправьте Ваше местоположение.",
        "REG_LOCATION_RECEIVED_MSG": "Ваше текущее местоположение:",
        "NO_ORDERS_FOUND_MSG": "😞 Заказы не найдены.",
        "OPTIONS_MSG": "Здесь Вы можете обратиться в службу поддержки, сменить язык и т.д.",
        "CUS_SUPPORT_MSG": "Задайте ваш вопрос:",
        "SUPPORT_FR_CUS_MSG": lambda
            customer_username,
            customer_id,
            req_text: f"❗️Новое входящие обращение от Пользователя @{customer_username}" \
                      f"({customer_id}):\n{req_text}",
        "SUPPORT_SENT_MSG": "Ваше обращение было отправлено в службу поддержки.\nСкоро с Вами свяжутся.",
        "LANG_SEL_MENU": "Меню выбора языка бота.",
        "CHANGE_LANG_MSG": "Выберете язык",
        "RESET_CONTACT_INFO_MSG": "⚠️ Вы уверены, что хотите сбросить свои контактные данные?",
        "CONTACT_INFO_DELETED_MSG": " ⚠️Ваши контактные данные удалены.",
        "DELETE_PROFILE_MSG": "⚠️ Вы уверены, что хотите удалить свой профиль?",
        "PROFILE_DELETED_MSG": "⚠️ Ваш профиль удален.",
        "EXITING_ORDER_MENU_MSG": "Возвращаемся в главное меню.",
        "DELETING_CART_ALERT": "⚠️ Ваша корзина удалена.",
        "GOING_BACK_MSG": "Возвращаемся назад...",
        "NO_COURIERS_MSG": "К сожалению, сейчас нет доступных курьеров, попробуйте снова.",
        "LOCATION_NOT_FOUND_MSG": "Контактные данные не найдены.\n"
                                  "Пожалуйста, обновите контактные данные.",
        "CONFIRM_LOCATION_MSG": "Это правильный адрес доставки?",
        "CHOOSE_REST_TYPE_MSG": "Пожалуйста, выберите тип заведения.",
        "REST_TYPE_SELECTED_MSG": lambda
            rest_type: f"Выбранный тип заведения:\n" \
                       f"{rest_type}",
        "CHOOSE_REST_MSG": "Выберите заведение.",
        "REST_SELECTED_MSG": lambda
            restaurant: f"Выбранное заведение:\n" \
                        f"{restaurant}",
        "CHOOSE_DISH_CATEGORY_MSG": "Пожалуйста, выберите категорию.",
        "DISH_CAT_SELECTED_MSG": lambda
            dish_cat: f"Выбранная категория:\n" \
                      f"{dish_cat}",
        "CHOOSE_DISH_MSG": "Выберите товар",
        "DISH_SELECTED_MSG": lambda
            dish: f"Выбранный товар:\n" \
                  f"{dish[0]}\n" \
                  f"Описание:\n" \
                  f"{dish[1]}\n" \
                  f"Цена:\n" \
                  f"€{dish[2]}",
        "ADD_DISH_MSG": "Добавить товар в корзину?",
        "YOUR_CART_MSG": lambda
            dishes,
            subtotal,
            courier_fee,
            service_fee,
            total: f"🛒 Ваша корзина:\n" \
                   f"{dishes}\n" \
                   f"Подытог:\n" \
                   f"€{subtotal}\n" \
                   f"Гонорар курьера:\n" \
                   f"€{courier_fee}\n" \
                   f"Сервисный сбор:\n" \
                   f"€{service_fee}\n" \
                   f"----\n" \
                   f"Итог:\n" \
                   f"€{total}",
        "CART_ACTIONS_MSG": "Действия:",
        "DELETE_ITEM_MSG": "Выберите товар для удаления",
        "MY_ORDERS_MSG": lambda
            orders,
            status: f"Номер заказа:\n`{orders[0][0]}`\n" \
                    f"из: {orders[0][1]}\n" \
                    f"Курьер: {orders[0][2]}\n" \
                    f"Товар(ы): {orders[0][3]}\n" \
                    f"Сумма: €{orders[0][4]}\n" \
                    f"Дата: {orders[0][5]}\n" \
                    f"Статус: {status}\n" \
                    f"Заказ закрыт:{orders[0][7]}",
        "STATUS_CODES": {
            "-1": "Отменен",
            "0": "Закрыт",
            "1": "Создан",
            "2": "Оплачен",
            "3": "Передан в ресторан, ищем курьера",
            "4": "Готовится, курьер найден",
            "5": "Готово, передаем курьеру",
            "6": "В доставке",
            "7": "Доставлен"
        },
        "ADD_COMMENT_MSG": "Добавьте комментарий к Вашему заказу:",
        "COMMENT_ADDED_MSG": "Ваш комментарий добавлен.",
        "TO_CART_MSG": "Вернуться в корзину?",
        "ORDER_CREATED_MSG": lambda
            order_info: f"Создан заказ:\n`{order_info[0]}`\n" \
                        f"Ресторан:\n{order_info[3]}\n" \
                        f"Товар(ы):\n{order_info[7]}\n" \
                        f"Сумма:\n€`{order_info[11]}`\n" \
                        f"Дата:\n{order_info[12]}\n" \
                        f"Комментарий:\n{order_info[14]}",
        "PAYMENT_MENU_MSG": lambda url: f"Пожалуйста, оплатите заказ по ссылке: {url}",
        "PAYPAL_ORDER_CREATION_FAIL_MSG": "Что-то пошло не так при создании ссылки для оплаты, пожалуйста, повторите попытку позднее.",
        "CUS_PAYMENT_CONFIRMED_MSG": lambda
            order_uuid: f"Оплата заказа\n" \
                        f"`{order_uuid}`\n" \
                        f"Подтверждена",
        "REST_ACCEPT_ORDER_BTN": "✅ Принять заказ",
        "WAIT_FOR_CONFIRMATION_MSG": lambda
            order_uuid: f"Подтверждение оплаты не получено\n" \
                        f"Заказ №\n`{order_uuid}`.",
        "ORDER_CLOSED_MSG": lambda order_uuid: f"Закрыт заказ:\n`{order_uuid}`",
        "CANCEL_MSG": lambda order_uuid: f"Заказ отменен\n`{order_uuid}`",
        "REST_NEW_ORDER_MSG": lambda
            order_uuid,
            dishes,
            subtotal,
            comment: f"Новый входящий заказ\n" \
                     f"`{order_uuid}`\n" \
                     f"Товар(ы):\n" \
                     f"{dishes}\n" \
                     f"К выплате:\n" \
                     f"`{subtotal}`\n" \
                     f"Комментарий:\n" \
                     f"{comment}"
    }
}
