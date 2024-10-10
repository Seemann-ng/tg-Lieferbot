from environs import Env

env = Env()
env.read_env()

texts = {
    "de_DE": {
        # Localization variables.
        "MAX_PHONE_LENGTH": 11,
        "COURIER_FEE_BASE": env.float("COURIER_FEE_BASE", default=1.15),
        "COURIER_FEE_RATE": env.float("COURIER_FEE_RATE", default=0.05),
        "SERVICE_FEE_BASE": env.float("SERVICE_FEE_BASE", default=0.75),
        "SERVICE_FEE_RATE": env.float("SERVICE_FEE_RATE", default=0.03),
        "AGREEMENT_MENU_PLACEHOLDER": "📑 Vereinbarung",
        # Menu buttons.
        "SHOW_AGREEMENT_BTN": "🔍📑 Kundenvereinbarung anzeigen",
        "ACCEPT_AGREEMENT_BTN": "📝 Kundenvereinbarung akzeptieren",
        "REG_PHONE_MENU_PLACEHOLDER": "📱 Eingabe der Telefonnummer",
        "REG_PHONE_MAN_BTN": "👨🏼‍💻 Telefonnummer manuell eingeben",
        "REG_PHONE_IMPORT_BTN": "⬆️ Telefonnummer aus Konto importieren",
        "REG_LOCATION_BTN": "🌍 Standort senden",
        "REG_LOCATION_PLACEHOLDER": "🌍 Standort",
        "MAIN_MENU_BTN": "🟰 Hauptmenü",
        "NEW_ORDER_BTN": "⭕️ Neue Bestellung",
        "MY_ORDERS_BTN": "📑 Meine Bestellungen",
        "OPTIONS_BTN": "🟰 Option",
        "CHANGE_LANG_BTN": "💬 Sprache auswahlen",
        "SEL_LANG_DE_BTN": "🇩🇪 Deutsch",
        "SEL_LANG_EN_BTN": "🇺🇸 Englisch\n(English)",
        "SEL_LANG_RU_BTN": "🇷🇺 Russisch\n(Русский)",
        "CONTACT_SUPPORT_BTN": "📞 Support kontaktieren\n🛠IN ENTWICKLUNG🛠",
        "RESET_CONTACT_INFO_BTN": "⚠️ Kontaktinformationen zurücksetzen",
        "CONFIRM_RESET_BTN": "✅ JA, meine Kontaktdaten zurücksetzen",
        "DELETE_PROFILE_BTN": "⚠️ Profil löschen",
        "CONFIRM_DELETE_PROFILE_BTN": "✅ JA, mein Profil löschen",
        "CONFIRM_LOCATION_BTN": "✅ Ja!",
        "WRONG_LOCATION_BTN": "❌ Nein.",
        "GO_BACK_BTN": "⬅️ Zurück",
        "CART_BTN": "🛒 Mein Einkaufskorb",
        "CANCEL_ORDER_BTN": "🚫 BESTELLUNG STORNIEREN",
        "ADD_DISH_BTN": "✅ In den Einkaufskorb",
        "PAY_BTN": "💳 Bestellung bestätigen\n🛠IN ENTWICKLUNG🛠",
        "ADD_MORE_BTN": "🛍 Weiter einkaufen",
        "DELETE_ITEM_BTN": "📤 Artikel löschen",
        "IN_DEV": "Ich habe dir gesagt, ES IST IN ENTWICKLUNG!",
        # Bot messages.
        "WELCOME_BACK_MSG": lambda customer_name: f"Willkommen zurück, {customer_name}!",
        "MAIN_MENU_MSG": "Sie befinden sich jetzt im Hauptmenü.",
        "FIRST_WELCOME_MSG": "Willkommen im %BOT_NAME%.",
        "ASK_AGREEMENT_MSG": "Um fortzufahren, müssen Sie unsere Kundenvereinbarung akzeptieren.",
        "AGREEMENT_TEXT": "MUSTERVERTRAGSTEXT.",
        "AGREEMENT_ACCEPTED_MSG": "✅ Kundenvereinbarung wurde akzeptiert.",
        "REG_NAME_MSG": "Wie heissen Sie?",
        "REG_NAME_PLACEHOLDER": "Ihr Name",
        "REG_NAME_RECEIVED_MSG": lambda new_name: f"Ihr Name wurde geändert in: {new_name}.",
        "REG_PHONE_METHOD_MSG": "Wie möchten Sie Ihre Telefonnummer angeben?",
        "REG_PHONE_MSG": "Bitte bieten Sie uns Ihre Telefon-Nummer (ohne '+'!).",
        "REG_PHONE_PLACEHOLDER": "Ihre Telefonnummer",
        "PHONE_RECEIVED_MSG": lambda phone_number: f"Ihre Telefonnummer wurde geändert in: {phone_number}.",
        "INVALID_PHONE_MSG": "‼️ Ungültige Telefonnummer.",
        "REG_LOCATION_MSG": "Bitte senden Sie Ihren Standort.",
        "REG_LOCATION_RECEIVED_MSG": "Ihr aktueller Standort ist:",
        "NO_ORDERS_FOUND_MSG": "😞 Es wurden keine Bestellungen gefunden.",
        "OPTIONS_MSG": "Hier können Sie den Support kontaktieren, Ihre Kontaktinformationen zurücksetzen oder löschen.",
        "LANG_SEL_MENU": "Menü zur Auswahl der Bot-Sprache.",
        "CHANGE_LANG_MSG": "Bot-Sprache auswählen",
        "RESET_CONTACT_INFO_MSG": "⚠️ Sind Sie sicher, dass Sie Ihre Kontaktinformationen zurücksetzen möchten?",
        "CONTACT_INFO_DELETED_MSG": "⚠️ Ihre Kontaktinformationen wurden gelöscht.",
        "DELETE_PROFILE_MSG": "⚠️ Sind Sie sicher, dass Sie Ihr Profil löschen möchten?",
        "PROFILE_DELETED_MSG": "⚠️ Ihr Profil wurde gelöscht.",
        "EXITING_ORDER_MENU_MSG": "Zurück zum Hauptmenü.",
        "DELETING_CART_ALERT": "⚠️ Ihr Einkaufskorb wurde geleert.",
        "GOING_BACK_MSG": "Zurück...",
        "LOCATION_NOT_FOUND_MSG": "Kontaktinformationen wurden nicht gefunden.\n"
                                  "Bitte setzen Sie Ihre Kontaktinformationen zurück.",
        "REQUEST_NEW_LOCATION_MSG": "Bitte setzen Sie Ihre Kontaktinformationen zurück.",
        "CONFIRM_LOCATION_MSG": "Ist diese Lieferadresse richtig?",
        "CHOOSE_REST_TYPE_MSG": "Bitte wählen Sie einen Restauranttyp.",
        "REST_TYPE_SELECTED_MSG": lambda rest_type: f"Ausgewählter Restauranttyp:\n"\
                                                    f"{rest_type}",
        "CHOOSE_REST_MSG": "Bitte wählen Sie ein Restaurant.",
        "REST_SELECTED_MSG": lambda restaurant: f"Ausgewähltes Restaurant:\n"\
                                                       f"{restaurant}",
        "CHOOSE_DISH_CATEGORY_MSG": "Bitte wählen Sie eine Gerichtskategorie.",
        "DISH_CAT_SELECTED_MSG": lambda dish_cat: f"Ausgewählte Gerichtskategorie:\n"\
                                                  f"{dish_cat}",
        "CHOOSE_DISH_MSG": "Bitte wählen Sie Ihr Gericht",
        "DISH_SELECTED_MSG": lambda lang_code, dish: f"Ausgewähltes Gericht:\n"\
                                                f"{dish[0]}\n"\
                                                f"Beschreibung:\n"\
                                                f"{dish[1]}\n"\
                                                f"Preis:\n"\
                                                f"€{dish[2]}",
        "ADD_DISH_MSG": "Gericht in den Warenkorb legen?",
        "YOUR_CART_MSG": lambda lang_code, dishes,
                                subtotal, courier_fee,
                                service_fee, total: f"🛒 Ihr Einkaufskorb:\n"\
                                                    f"{dishes}\n"\
                                                    f"Zwischensummen:\n"\
                                                    f"€{subtotal}\n"\
                                                    f"Kuriergebühr:\n"\
                                                    f"€{courier_fee}\n"\
                                                    f"Servicegebühr:\n"\
                                                    f"€{service_fee}\n"\
                                                    f"----\n"\
                                                    f"Insgesamt:\n"\
                                                    f"€{total}",
        "CART_ACTIONS_MSG": "Aktionen:",
        "DELETE_ITEM_MSG": "Zu löschende Element auswählen",
        "MY_ORDERS_MSG": lambda orders: "Sie haben noch keine Bestellungen." if not orders\
                                        else f"Bestellnummer: {orders[0][0][-6:]}\n"\
                                             f"von: {orders[0][1]}\n"\
                                             f"Kurier: {orders[0][2]}\n"\
                                             f"Gericht(e): {orders[0][3]}\n"\
                                             f"Gesamtkosten: €{orders[0][4]}\n"\
                                             f"Datum: {orders[0][5]}\n"\
                                             f"Status: {orders[0][6]}"
    },
    "en_US": {
        # Localization variables.
        "MAX_PHONE_LENGTH": 11,
        "COURIER_FEE_BASE": env.float("COURIER_FEE_BASE", default=2.25),
        "COURIER_FEE_RATE": env.float("COURIER_FEE_RATE", default=0.08),
        "SERVICE_FEE_BASE": env.float("SERVICE_FEE_BASE", default=1.75),
        "SERVICE_FEE_RATE": env.float("SERVICE_FEE_RATE", default=0.05),
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
        "CONTACT_SUPPORT_BTN": "📞 Contact support\n🛠IN DEVELOPMENT🛠",
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
        "PAY_BTN": "💳 Confirm order\n🛠IN DEVELOPMENT🛠",
        "ADD_MORE_BTN": "🛍 Continue shopping",
        "DELETE_ITEM_BTN": "📤 Delete item",
        "IN_DEV": "I've told You, IT IS IN DEVELOPMENT!",
        # Bot messages.
        "WELCOME_BACK_MSG": lambda customer_name: f"Welcome back, {customer_name}!",
        "MAIN_MENU_MSG": "You're in main menu now.",
        "FIRST_WELCOME_MSG": "Welcome to the %BOT_NAME%.",
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
        "LANG_SEL_MENU": "Bot language selection menu.",
        "CHANGE_LANG_MSG": "Select bot language",
        "RESET_CONTACT_INFO_MSG": "⚠️ Are You sure You want to reset Your contact info?",
        "CONTACT_INFO_DELETED_MSG": " ⚠️Your contact info were deleted.",
        "DELETE_PROFILE_MSG": "⚠️ Are You sure You want to delete Your profile?",
        "PROFILE_DELETED_MSG": "⚠️ Your profile has been deleted.",
        "EXITING_ORDER_MENU_MSG": "Going back to main menu.",
        "DELETING_CART_ALERT": "⚠️ Your cart was cleared.",
        "GOING_BACK_MSG": "Going back...",
        "LOCATION_NOT_FOUND_MSG": "Contact information wasn't found.\n"
                                  "Please, reset Your contact information.",
        "REQUEST_NEW_LOCATION_MSG": "Please, reset Your contact information.",
        "CONFIRM_LOCATION_MSG": "Is this delivery address right?",
        "CHOOSE_REST_TYPE_MSG": "Please, choose a restaurant type.",
        "REST_TYPE_SELECTED_MSG": lambda rest_type: f"Selected restaurant type:\n"\
                                                    f"{rest_type}",
        "CHOOSE_REST_MSG": "Please, choose a restaurant.",
        "REST_SELECTED_MSG": lambda restaurant: f"Selected restaurant:\n"\
                                                f"{restaurant}",
        "CHOOSE_DISH_CATEGORY_MSG": "Please, choose a dish category.",
        "DISH_CAT_SELECTED_MSG": lambda dish_cat: f"Selected dish category:\n"\
                                                  f"{dish_cat}",
        "CHOOSE_DISH_MSG": "Please, choose Your dish",
        "DISH_SELECTED_MSG": lambda lang_code, dish: f"Selected dish:\n"\
                                                     f"{dish[0]}\n"\
                                                     f"Description:\n"\
                                                     f"{dish[1]}\n"\
                                                     f"Price:\n"\
                                                     f"€{dish[2]}",
        "ADD_DISH_MSG": "Add dish to the cart?",
        "YOUR_CART_MSG": lambda lang_code, dishes,
                                subtotal, courier_fee,
                                service_fee, total: f"🛒 Your cart:\n"\
                                                    f"{dishes}\n"\
                                                    f"Subtotal:\n"\
                                                    f"€{subtotal}\n"\
                                                    f"Courier fee:\n"\
                                                    f"€{courier_fee}\n"\
                                                    f"Service fee:\n"\
                                                    f"€{service_fee}\n"\
                                                    f"----\n"\
                                                    f"Total:\n"\
                                                    f"€{total}",
        "CART_ACTIONS_MSG": "Actions:",
        "DELETE_ITEM_MSG": "Choose item to delete",
        "MY_ORDERS_MSG": lambda orders: "You have no orders yet." if not orders\
                                        else f"Order Number: {orders[0][0][-6:]}\n"\
                                             f"from: {orders[0][1]}\n"\
                                             f"Courier: {orders[0][2]}\n"\
                                             f"Dish(es): {orders[0][3]}\n"\
                                             f"Total: €{orders[0][4]}\n"\
                                             f"Date: {orders[0][5]}\n"\
                                             f"Status: {orders[0][6]}"
    },
    "ru_RU": {  # TODO Translate
        # Localization variables.
        "MAX_PHONE_LENGTH": 11,
        "COURIER_FEE_BASE": env.float("COURIER_FEE_BASE", default=2.25),
        "COURIER_FEE_RATE": env.float("COURIER_FEE_RATE", default=0.08),
        "SERVICE_FEE_BASE": env.float("SERVICE_FEE_BASE", default=1.75),
        "SERVICE_FEE_RATE": env.float("SERVICE_FEE_RATE", default=0.05),
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
        "SEL_LANG_DE_BTN": "🇩🇪 Немецкий\n(Deutsch)",
        "SEL_LANG_EN_BTN": "🇺🇸 Английский\n(English)",
        "SEL_LANG_RU_BTN": "🇷🇺 Русский",
        "CONTACT_SUPPORT_BTN": "📞 Contact support\n🛠IN DEVELOPMENT🛠",
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
        "PAY_BTN": "💳 Confirm order\n🛠IN DEVELOPMENT🛠",
        "ADD_MORE_BTN": "🛍 Continue shopping",
        "DELETE_ITEM_BTN": "📤 Delete item",
        "IN_DEV": "I've told You, IT IS IN DEVELOPMENT!",
        # Bot messages.
        "WELCOME_BACK_MSG": lambda customer_name: f"Welcome back, {customer_name}!",
        "MAIN_MENU_MSG": "You're in main menu now.",
        "FIRST_WELCOME_MSG": "Welcome to the %BOT_NAME%.",
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
        "LANG_SEL_MENU": "Bot language selection menu.",
        "CHANGE_LANG_MSG": "Select bot language",
        "RESET_CONTACT_INFO_MSG": "⚠️ Are You sure You want to reset Your contact info?",
        "CONTACT_INFO_DELETED_MSG": " ⚠️Your contact info were deleted.",
        "DELETE_PROFILE_MSG": "⚠️ Are You sure You want to delete Your profile?",
        "PROFILE_DELETED_MSG": "⚠️ Your profile has been deleted.",
        "EXITING_ORDER_MENU_MSG": "Going back to main menu.",
        "DELETING_CART_ALERT": "⚠️ Your cart was cleared.",
        "GOING_BACK_MSG": "Going back...",
        "LOCATION_NOT_FOUND_MSG": "Contact information wasn't found.\n"
                                  "Please, reset Your contact information.",
        "REQUEST_NEW_LOCATION_MSG": "Please, reset Your contact information.",
        "CONFIRM_LOCATION_MSG": "Is this delivery address right?",
        "CHOOSE_REST_TYPE_MSG": "Please, choose a restaurant type.",
        "REST_TYPE_SELECTED_MSG": lambda rest_type: f"Selected restaurant type:\n"\
                                                    f"{rest_type}",
        "CHOOSE_REST_MSG": "Please, choose a restaurant.",
        "REST_SELECTED_MSG": lambda restaurant: f"Selected restaurant:\n"\
                                                f"{restaurant}",
        "CHOOSE_DISH_CATEGORY_MSG": "Please, choose a dish category.",
        "DISH_CAT_SELECTED_MSG": lambda dish_cat: f"Selected dish category:\n"\
                                                  f"{dish_cat}",
        "CHOOSE_DISH_MSG": "Please, choose Your dish",
        "DISH_SELECTED_MSG": lambda lang_code, dish: f"Selected dish:\n"\
                                                     f"{dish[0]}\n"\
                                                     f"Description:\n"\
                                                     f"{dish[1]}\n"\
                                                     f"Price:\n"\
                                                     f"€{dish[2]}",
        "ADD_DISH_MSG": "Add dish to the cart?",
        "YOUR_CART_MSG": lambda lang_code, dishes,
                                subtotal, courier_fee,
                                service_fee, total: f"🛒 Your cart:\n"\
                                                    f"{dishes}\n"\
                                                    f"Subtotal:\n"\
                                                    f"€{subtotal}\n"\
                                                    f"Courier fee:\n"\
                                                    f"€{courier_fee}\n"\
                                                    f"Service fee:\n"\
                                                    f"€{service_fee}\n"\
                                                    f"----\n"\
                                                    f"Total:\n"\
                                                    f"€{total}",
        "CART_ACTIONS_MSG": "Actions:",
        "DELETE_ITEM_MSG": "Choose item to delete",
        "MY_ORDERS_MSG": lambda orders: "You have no orders yet." if not orders\
                                        else f"Order Number: {orders[0][0][-6:]}\n"\
                                             f"from: {orders[0][1]}\n"\
                                             f"Courier: {orders[0][2]}\n"\
                                             f"Dish(es): {orders[0][3]}\n"\
                                             f"Total: €{orders[0][4]}\n"\
                                             f"Date: {orders[0][5]}\n"\
                                             f"Status: {orders[0][6]}"
    }
}