# 🛒 Telegram Lieferbot

![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![image](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)

Delivery service based on the system of Telegram bots with integrated payments via PayPal.

## 🚀 Build and run:

Run the following command to start the Service:

```bash
docker compose up -d --build
```

## 🔐 Environment:

In the `.env` file, or through the `-e` flags, you must set the required variables from
tables below.

| Variable             | Default                 | Description                                                                        |
|----------------------|-------------------------|------------------------------------------------------------------------------------|
| CUSTOMER_BOT_TOKEN   | **(required)**          | Telegram bot token for Customer bot.                                               |
| RESTAURANT_BOT_TOKEN | **(required)**          | Telegram bot token for Restaurant bot.                                             |
| COURIER_BOT_TOKEN    | **(required)**          | Telegram bot token for Courier bot.                                                |
| ADMIN_BOT_TOKEN      | **(required)**          | Telegram bot token for Admin bot.                                                  |
| DB_USER              | **(required)**          | PostgreSQL DB username.                                                            |
| DB_PASSWORD          | **(required)**          | PostgreSQL DB user password.                                                       |
| DB_EXT_PORT          | **5432**                | External DB host port.                                                             |
| DEF_LANG             | **en_US**               | Default language of the bots (`en_US`, `de_DE`, `ru_RU` available).                |
| COURIER_FEE_BASE     | **2.25**                | (see remark below)                                                                 |
| COURIER_FEE_RATE     | **0.08**                | (see remark below)                                                                 |
| SERVICE_FEE_BASE     | **1.75**                | (see remark below)                                                                 |
| SERVICE_FEE_RATE     | **0.05**                | (see remark below)                                                                 |
| PP_USERNAME          | **(required)**          | PayPal app Client ID.                                                              |
| PP_PASSWORD          | **(required)**          | PayPal app secret key.                                                             |
| PP_MODE              | **sandbox**             | PayPal mode, `deployment` for real money transactions, `sandbox` for sandbox mode. |
| BRAND_NAME           | **Shop**                | Name of the Service displayed on PayPal payment page.                              |
| RETURN_LINK          | **https://google.com/** | URL Customer to be redirected to after payment completion on PayPal payment page.  |

__REMARK:__

Total price for the Customer is being calculated as per following formula:

`TOTAL = SUBTOTAL + COURIER_FEE + SERVICE_FEE`

Where:

`COURIER_FEE = SUBTOTAL * COURIER_FEE_RATE + COURIER_FEE_DISTANCE_RATE * DELIVERY_DISTANCE + COURIER_FEE_BASE`

AND

`SERVICE_FEE = SUBTOTAL * SERVICE_FEE_RATE + SERVICE_FEE_BASE`

## 🤖 Interaction with the bots:

To be described in README's in corresponding bots' directories.

## 👨‍🔧Built with:

* [Python 3.12](https://www.python.org/) - programming language.
* [PyCharm](https://www.jetbrains.com/pycharm/) - IDE from JetBrains.

## 👨‍💻 Author:

* **Ilia Tashkenov (_セーラー_)** - [Seemann-ng](https://github.com/Seemann-ng), 2024.

## 📝 License:

This project is licensed under the MIT License - see the [license website](https://opensource.org/licenses/MIT) for details.
