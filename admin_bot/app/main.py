import telebot.types as types

import tools.pp_tools as paypal
from admin_translations import texts as texts
from admin_db_tools import Interface as DBInterface
from tools.logger_tool import logger, logger_decorator_msg
from tools.bots_initialization import adm_bot, courier_bot


@adm_bot.message_handler(commands=["start"])
@logger_decorator_msg
def start_command(message: types.Message) -> None:
    """Process /start command.

    Args:
        message: /start command message.

    """
    msg = DBInterface(message)
    if not msg.is_admin():
        adm_bot.send_message(
            msg.data_to_read.from_user.id,
            texts[msg.get_admin_lang()]["NOT_REG_MSG"]
            )
        return None
    adm_bot.send_message(
        msg.data_to_read.from_user.id,
        texts[msg.get_admin_lang()]["WELCOME_MSG"]
    )


@adm_bot.message_handler(commands=["pay_salaries"])
@logger_decorator_msg
def pay_salaries_command(message: types.Message) -> None:
    """Process /pay_salaries command.

    Args:
        message: /pay_salaries command message.

    """
    msg = DBInterface(message)
    if not msg.is_admin():
        adm_bot.send_message(
            msg.data_to_read.from_user.id,
            texts[msg.get_admin_lang()]["NOT_REG_MSG"]
        )
        return None
    couriers = msg.get_couriers()
    if not couriers:
        adm_bot.send_message(
            msg.data_to_read.from_user.id,
            texts[msg.get_admin_lang()]["NO_COURIERS_MSG"]
        )
    for courier in couriers:
        if paypal.pp_courier_payout(courier) == 201:
            adm_bot.send_message(
                msg.data_to_read.from_user.id,
                texts[msg.get_admin_lang()]["SALARY_PAID_MSG"](courier)
            )
            courier_bot.send_message(
                courier[0],
                texts[courier[5]]["COUR_SALARY_PAID_MSG"](courier)
            )
        else:
            adm_bot.send_message(
                msg.data_to_read.from_user.id,
                texts[msg.get_admin_lang()]["PAYMENT_FAILED_MSG"](courier)
            )


def main():
    logger.info("Bot is running")
    adm_bot.infinity_polling()


if __name__ == '__main__':
    main()
