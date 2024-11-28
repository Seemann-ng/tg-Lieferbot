# 🧑‍🍳 LieferBot-Restaurant

Demo available [here](https://t.me/lrest_test_bot).

## 🤖 Interaction with the bot:

When `/start` command is sent, if User isn't registered in the database as a Restaurant account, bot sends registration request to User.
If Restaurant sends `/open_shift` command, they will receive incoming orders from Customers until `/close_shift` command is sent.
Then Restaurant should navigate through bot's workflow via appearing instructions and context menus.

__Commands:__

`/start` - Start interaction with the bot.

`/select_language` - Call language selection menu.

`/item_available` - Mark item as available.

`/item_unavailable` - Mark item as unavailable.

`/add_item ITEM NAME` - Add new item into menu.

`/edit_item` - Call item edition menu.

`/delete_item` - Call item deletion menu.

`/open_shift` - Set Restaurant status as open.

`/close_shift` - Set Restaurant status as closed.

`/support` - Send support request.

__Bot is available in English, German and Russian.__

## 👨‍🔧 Built with:

* [Python 3.12](https://www.python.org/) - programming language.
* [PyCharm](https://www.jetbrains.com/pycharm/) - IDE from JetBrains.

## 👨‍💻 Author:

* **Ilia Tashkenov (_セーラー_)** - [Seemann-ng](https://github.com/Seemann-ng), 2024.

## 📝 License:

This project is licensed under the MIT License - see the [license website](https://opensource.org/licenses/MIT) for details.
