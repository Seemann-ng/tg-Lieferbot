import functools

import psycopg2
from environs import Env

env = Env()
env.read_env()

DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")


def cursor(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(
            database="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host="liefer_bot_db",
            port=5432
        )
        curs = conn.cursor()
        result = func(*args, **kwargs, curs=curs)
        conn.commit()
        conn.close()
        return result

    return wrapper
