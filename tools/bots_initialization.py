import telebot as tb
from environs import Env

env = Env()
env.read_env()

CUSTOMER_BOT_TOKEN = env.str("CUSTOMER_BOT_TOKEN")
RESTAURANT_BOT_TOKEN = env.str("RESTAURANT_BOT_TOKEN")
COURIER_BOT_TOKEN = env.str("COURIER_BOT_TOKEN")
ADMIN_BOT_TOKEN = env.str("ADMIN_BOT_TOKEN")

cus_bot = tb.TeleBot(token=CUSTOMER_BOT_TOKEN, parse_mode="markdown")
rest_bot = tb.TeleBot(token=RESTAURANT_BOT_TOKEN, parse_mode="markdown")
courier_bot = tb.TeleBot(token=COURIER_BOT_TOKEN, parse_mode="markdown")
adm_bot = tb.TeleBot(token=ADMIN_BOT_TOKEN, parse_mode="markdown")
