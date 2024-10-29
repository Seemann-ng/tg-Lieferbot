# 🛵 LieferBot-Courier

Demo available [here](https://t.me/lcur_test_bot).

## 🤖 Interaction with the bot:

If Courier sends `/open_shift` command, they will receive incoming orders until `/close_shift` command is sent.
Then Courier should navigate through bot's workflow via appearing instructions and context menus.

__Commands:__

`/start` - Start interaction with the bot; if User is not registered in the Database as a Courier, bot will send a registration request.

`/select_language` - Call language selection menu.

`/balance` - Show current salary balance.

`/change_transport` - Call transport type selection menu.

`/open_shift` - Mark courier as currently working.

`/close_shift` - Mark courier as not currently working.

`/support` - Send support request.

__Bot is available in English, German and Russian.__

## 👨‍🔧 Built with:

* [Python 3.12](https://www.python.org/) - programming language.
* [PyCharm](https://www.jetbrains.com/pycharm/) - IDE from JetBrains.

## 👨‍💻 Author:

* **Ilia Tashkenov (_セーラー_)** - [Seemann-ng](https://github.com/Seemann-ng), 2024.

## 📝 License:

This project is licensed under the MIT License - see the [license website](https://opensource.org/licenses/MIT) for details.
