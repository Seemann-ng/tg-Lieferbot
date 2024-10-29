texts = {
    "en_US": {
        "WELCOME_MSG": "Welcome back!",
        "NOT_REG_MSG": "This Telegram account is not registered as Admin!.",
        "NO_COURIERS_MSG": "No unpaid courier salaries found!",
        "SALARY_PAID_MSG": lambda
            courier: f"Salary paid:\n" \
                     f"Courier: {courier[2]}\n" \
                     f"Telegram Username: `@{courier[1]}`\n" \
                     f"Telegram ID: {courier[0]}\n" \
                     f"Amount: €{courier[3]}",
        "COUR_SALARY_PAID_MSG": lambda courier: f"‼️ Salary paid:\nAmount: €{courier[3]} ‼️",
        "PAYMENT_FAILED_MSG": lambda
            courier: f"‼️ __PAYMENT FAILED__ ‼️\n" \
                     f"Courier: {courier[2]}\n" \
                     f"Telegram Username: `@{courier[1]}`\n" \
                     f"Telegram ID: {courier[0]}\n" \
                     f"Amount: €{courier[3]}"
    },
    "de_DE": {
        "WELCOME_MSG": "Willkommen zurück!",
        "NOT_REG_MSG": "Dieses Telegram-Konto ist nicht als Admin registriert!",
        "NO_COURIERS_MSG": "Keine unbezahlten Kuriergehälter gefunden!",
        "SALARY_PAID_MSG": lambda
            courier: f"Gehalt bezahlt:\n" \
                     f"Kurier: {courier[2]}\n" \
                     f"Telegram-Benutzername: `@{courier[1]}`\n" \
                     f"Telegram-ID: {courier[0]}\n" \
                     f"Betrag: €{courier[3]}",
        "COUR_SALARY_PAID_MSG": lambda courier: f"‼️ Gehalt bezahlt:\nBetrag: €{courier[3]} ‼️",
        "PAYMENT_FAILED_MSG": lambda
            courier: f"‼️ ZAHLUNG FEHLGESCHLAGEN ‼️\n" \
                     f"Kurier: {courier[2]}\n" \
                     f"Telegram-Benutzername: `@{courier[1]}`\n" \
                     f"Telegram-ID: {courier[0]}\n" \
                     f"Betrag: €{courier[3]}"
    },
    "ru_RU": {
        "WELCOME_MSG": "С возвращением!",
        "NOT_REG_MSG": "Этот аккаунт Telegram не зарегистрирован как Администратор!",
        "NO_COURIERS_MSG": "Не найдено непогашенных зарплат для курьеров!",
        "SALARY_PAID_MSG": lambda
            courier: f"Зарплата выплачена:\n" \
                     f"Курьер: {courier[2]}\n" \
                     f"Имя пользователя Telegram: `@{courier[1]}`\n" \
                     f"Telegram ID: {courier[0]}\n" \
                     f"Сумма: €{courier[3]}",
        "COUR_SALARY_PAID_MSG": lambda courier: f"‼️ Зарплата выплачена:\nСумма: €{courier[3]} ‼️",
        "PAYMENT_FAILED_MSG": lambda
            courier: f"‼️ ОПЛАТА НЕ ПРОШЛА ‼️\n" \
                     f"Курьер: {courier[2]}\n" \
                     f"Имя пользователя Telegram: `@{courier[1]}`\n" \
                     f"Telegram ID: {courier[0]}\n" \
                     f"Сумма: €{courier[3]}"}
}