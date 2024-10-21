# 🛒 Telegram Lieferbot

![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![image](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)

Delivery service based on the system of Telegram bots with integrated payments via PayPal.

## 💾 Build and run:

Run the following command to start the Service:

```bash
docker compose up -d --build
```

## 🔐 Environment:

In the `.env` file, or through the `-e` flags, you must set the required variables from
tables below.

| Variable             | Default        | Description                                                                                                          |
|----------------------|----------------|----------------------------------------------------------------------------------------------------------------------|
| CUSTOMER_BOT_TOKEN   | **(required)** | Telegram bot token for Customer bot.                                                                                 |
| RESTAURANT_BOT_TOKEN | **(required)** | Telegram bot token for Restaurant bot.                                                                               |
| COURIER_BOT_TOKEN    | **(required)** | Telegram bot token for Courier bot.                                                                                  |
| ADMIN_BOT_TOKEN      | **(required)** | Telegram bot token for Admin bot.                                                                                    |
| DB_USER              | **(required)** | PostgreSQL DB username.                                                                                              |
| DB_PASSWORD          | **(required)** | PostgreSQL DB user password.                                                                                         |
| DB_EXT_PORT          | **(optional)** | External DB host port, defaults to `5432`.                                                                           |
| DEF_LANG             | **(optional)** | Default language of the bots, defaults to __en_US__.                                                                 |
| COURIER_FEE_BASE     | **(optional)** | Defaults to __2.25__ _(see remark below)._                                                                           |
| COURIER_FEE_RATE     | **(optional)** | Defaults to __0.08__ _(see remark below)._                                                                           |
| SERVICE_FEE_BASE     | **(optional)** | Defaults to __1.75__ _(see remark below)._                                                                           |
| SERVICE_FEE_RATE     | **(optional)** | Defaults to __0.05__ _(see remark below)._                                                                           |
| PP_USERNAME          | **(required)** | PayPal app Client ID.                                                                                                |
| PP_PASSWORD          | **(required)** | PayPal app secret key.                                                                                               |
| PP_MODE              | **(optional)** | PayPal mode, `deployment` for real money transactions, `sandbox` for sandbox mode, defaults to `sandbox`.            |
| BRAND_NAME           | **(optional)** | Name of the Service displayed on PayPal payment page.                                                                |
| RETURN_LINK          | **(optional)** | URL Customer to be redirected to after payment completion on PayPal payment page, defaults to `https://google.com/`. |

__REMARK:__

Total price for the Customer is being calculated as per following formula:

__TOTAL__ = __SUBTOTAL__ + __COURIER_FEE__ + __SERVICE_FEE__

Where:

__COURIER_FEE__ = __SUBTOTAL__ * __COURIER_FEE_RATE__ + __COURIER_FEE_BASE__

AND

__SERVICE_FEE__ = __SUBTOTAL__ * __SERVICE_FEE_RATE__ + __SERVICE_FEE_BASE__

## 🤖 Interaction with the bots:

To be described in README's in corresponding bots' directories.

## 👨‍🔧Built with:

* [Python 3.12](https://www.python.org/) - programming language.
* [PyCharm](https://www.jetbrains.com/pycharm/) - IDE from JetBrains.

## 👨‍💻 Author:

* **Ilia Tashkenov (_セーラー_)** - [Seemann-ng](https://github.com/Seemann-ng), 2024.

## 📝 License:

This project is licensed under the MIT License - see the [license website](https://opensource.org/licenses/MIT) for details.
