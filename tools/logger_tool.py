import logging
import functools

import telebot.types as types

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def logger_decorator_msg(func):
    @functools.wraps(func)
    def wrapper(message: types.Message):
        logger.info(
            f"Function {func.__name__} called by user {message.from_user.username} by message {message.text}."
        )
        result = func(message)
        logger.info(f"Function {func.__name__} executed successfully.")
        return result
    return wrapper


def logger_decorator_callback(func):
    @functools.wraps(func)
    def wrapper(call: types.CallbackQuery):
        logger.info(
            f"Function {func.__name__} called by user {call.from_user.username} by callback query {call.data}."
        )
        result = func(call)
        logger.info(f"Function {func.__name__} executed successfully.")
        return result
    return wrapper


def logger_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(
            f"Function {func.__name__} called."
        )
        result = func(*args, **kwargs)
        logger.info(f"Function {func.__name__} executed successfully.")
        return result
    return wrapper
