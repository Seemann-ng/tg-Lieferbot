# Menu buttons.
AGREEMENT_MENU_PLACEHOLDER = "📑 Vereinbarung"
SHOW_AGREEMENT_BTN = "🔍📑 Kundenvereinbarung anzeigen"
ACCEPT_AGREEMENT_BTN = "📝 Kundenvereinbarung akzeptieren"
REG_PHONE_MENU_PLACEHOLDER = "📱 Eingabe der Telefonnummer"
REG_PHONE_MAN_BTN = "👨🏼‍💻 Telefonnummer manuell eingeben"
REG_PHONE_IMPORT_BTN = "⬆️ Telefonnummer aus Konto importieren"
REG_LOCATION_BTN = "🌍 Standort senden"
REG_LOCATION_PLACEHOLDER = "🌍 Standort"
MAIN_MENU_BTN = "🟰 Hauptmenü"
NEW_ORDER_BTN = "⭕️ Neue Bestellung"
MY_ORDERS_BTN = "📑 Meine Bestellungen"
OPTIONS_BTN = "🟰 Option"
CONTACT_SUPPORT_BTN = "📞 Support kontaktieren\n🛠IN ENTWICKLUNG🛠"
RESET_CONTACT_INFO_BTN = "⚠️ Kontaktinformationen zurücksetzen"
CONFIRM_RESET_BTN = "✅ JA, meine Kontaktdaten zurücksetzen"
DELETE_PROFILE_BTN = "⚠️ Profil löschen"
CONFIRM_DELETE_PROFILE_BTN = "✅ JA, mein Profil löschen"
CONFIRM_LOCATION_BTN = "✅ Ja!"
WRONG_LOCATION_MSG = "❌ Nein."
GO_BACK_BTN = "⬅️ Zurück"
CART_BTN = "🛒 Mein Einkaufswagen"
CANCEL_ORDER_BTN = "🚫 BESTELLUNG STORNIEREN"
ADD_DISH_BTN = "✅ In den Einkaufswagen"
PAY_BTN = "💳 Bestellung bestätigen"
ADD_MORE_BTN = "🛍 Weiter einkaufen"
DELETE_ITEM_BTN = "📤 Artikel löschen"

# Localization variables.
PHONE_NUM_PREFIX = "+49"
MAX_PHONE_LENGTH_WO_PREFIX = 11
CURRENCY = "€"

# Bot messages.
IN_DEV = "Ich habe dir gesagt, ES IST IN ENTWICKLUNG!"
WELCOME_BACK_MSG = "Willkommen zurück, "
MAIN_MENU_MSG = "Sie befinden sich jetzt im Hauptmenü."
FIRST_WELCOME_MSG = "Willkommen im %BOT_NAME%."
ASK_AGREEMENT_MSG = "Um fortzufahren, müssen Sie unsere Kundenvereinbarung akzeptieren."
AGREEMENT_TEXT = "MUSTERVERTRAGSTEXT."
AGREEMENT_ACCEPTED_MSG = "✅ Kundenvereinbarung wurde akzeptiert."
REG_NAME_MSG = "Wie heissen Sie?"
REG_NAME_PLACEHOLDER = "Ihr Name"
REG_NAME_RECEIVED_MSG = "Ihr Name wurde geändert in: "
REG_PHONE_METHOD_MSG = "Wie möchten Sie Ihre Telefonnummer angeben?"
REG_PHONE_MSG = f"Bitte bieten Sie uns Ihre Telefon-Nummer (ohne '{PHONE_NUM_PREFIX}'!)."
REG_PHONE_PLACEHOLDER = "Ihre Telefonnummer"
PHONE_RECEIVED_MSG = "Ihre Telefonnummer wurde geändert in: "
INVALID_PHONE_MSG = "‼️ Ungültige Telefonnummer."
REG_LOCATION_MSG = "Bitte senden Sie Ihren Standort."
REG_LOCATION_RECEIVED_MSG = "Ihr aktueller Standort ist:"
NO_ORDERS_FOUND_MSG = "😞 Es wurden keine Bestellungen gefunden."
OPTIONS_MSG = "Hier können Sie den Support kontaktieren, Ihre Kontaktinformationen zurücksetzen oder löschen."
RESET_CONTACT_INFO_MSG = "⚠️ Sind Sie sicher, dass Sie Ihre Kontaktinformationen zurücksetzen möchten?"
CONTACT_INFO_DELETED_MSG = "⚠️ Ihre Kontaktinformationen wurden gelöscht."
DELETE_PROFILE_MSG = "⚠️ Sind Sie sicher, dass Sie Ihr Profil löschen möchten?"
PROFILE_DELETED_MSG = "⚠️ Ihr Profil wurde gelöscht."
EXITING_ORDER_MENU_MSG = "Zurück zum Hauptmenü."
DELETING_CART_ALERT = "⚠️ Ihr Einkaufswagen wurde geleert."
GOING_BACK_MSG = "Zurück..."
LOCATION_NOT_FOUND_MSG = f"Kontaktinformationen wurden nicht gefunden.\n"\
                         f"Bitte setzen Sie Ihre Kontaktinformationen zurück.\n"\
                         f"(\'{OPTIONS_BTN}\' -> \'{RESET_CONTACT_INFO_BTN}\')"
REQUEST_NEW_LOCATION_MSG = f"Bitte setzen Sie Ihre Kontaktinformationen zurück.\n"\
                         f"(\'{OPTIONS_BTN}\' -> \'{RESET_CONTACT_INFO_BTN}\')"
CONFIRM_LOCATION_MSG = "Ist diese Lieferadresse richtig?"
CHOOSE_REST_TYPE_MSG = "Bitte wählen Sie einen Restauranttyp."
SELECTED_REST_TYPE_MSG = "Ausgewählter Restauranttyp:"
CHOOSE_REST_MSG = "Bitte wählen Sie ein Restaurant."
SELECTED_REST_MSG = "Ausgewähltes Restaurant:"
CHOOSE_DISH_CATEGORY_MSG = "Bitte wählen Sie eine Gerichtskategorie."
SELECTED_DISH_CAT_MSG = "Ausgewählte Gerichtskategorie:"
CHOOSE_DISH_MSG = "Bitte wählen Sie Ihr Gericht"
SELECTED_DISH_MSG = "Ausgewähltes Gericht:"
DISH_DESC_MSG = "Beschreibung:"
DISH_PRICE_MSG = "Preis:"
YOUR_CART_MSG = "🛒 Ihr Einkaufswagen"
SUBTOTAL_MSG = "Zwischensummen:"


def my_orders_msg(orders: list) -> str:  # TODO: lambda
    if not orders:
        return "Sie haben noch keine Bestellungen."
    order_id = orders[0][0][-6:]
    order_from = orders[0][1]
    courier_name = orders[0][2]
    dishes = orders[0][3]
    total = orders[0][4]
    order_date = orders[0][5]
    order_status = orders[0][6]
    orders.pop(0)
    msg = (f"Bestellnummer: {order_id}\n"
           f"von: {order_from}\n"
           f"Kurier: {courier_name}\n"
           f"Gericht(e): {dishes}\n"
           f"Gesamtkosten: {CURRENCY}{total}\n"
           f"Datum: {order_date}\n"
           f"Status: {order_status}\n")
    return msg
