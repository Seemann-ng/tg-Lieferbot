from tools.logger_tool import logger
from tools.bots_initialization import adm_bot


def main():
    logger.info("Bot is running")
    adm_bot.infinity_polling()


if __name__ == '__main__':
    main()
