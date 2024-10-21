import json
import requests
from typing import Dict

import psycopg2
from environs import Env

from tools.cursor_tool import cursor
from tools.logger_tool import logger, logger_decorator

env = Env()
env.read_env()

pp_mode = env.str("PP_MODE", default="sandbox")
pp_username = env.str("PP_USERNAME")
pp_password = env.str("PP_PASSWORD")
brand_name = env.str("BRAND_NAME")
return_link = env.str("RETURN_LINK")

@cursor
@logger_decorator
def pp_order_creation(order_uuid: str, curs: psycopg2.extensions.cursor) -> Dict[str, str]:
    """

    Args:
        order_uuid:
        curs:

    Returns:

    """  # TODO
    if pp_mode == "deployment":
        url = "https://api-m.paypal.com/v2/checkout/orders"
    else:
        url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
    curs.execute("SELECT total FROM orders WHERE order_uuid = %s", (order_uuid,))
    transaction_amount = str(curs.fetchone()[0])
    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "EUR",
                    "value": transaction_amount
                }
            }
        ],
        "payment_source": {
            "paypal": {
                "experience_context": {
                    "brand_name": brand_name,
                    "landing_page": "NO_PREFERENCE",
                    "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                    "locale": "de-DE",
                    "user_action": "PAY_NOW",
                    "return_url": return_link,
                    "cancel_url": return_link
                }
            }
        }
    }
    response = requests.post(url, json=data, auth=(pp_username, pp_password))
    if response.status_code == 200 and json.loads(response.text)["status"] == "PAYER_ACTION_REQUIRED":
        order_id = json.loads(response.text)["id"]
        logger.info(f"PayPal order created. Order ID: {order_id}")
        return {"URL": json.loads(response.text)["links"][1]["href"], "order_id": order_id}
    else:
        logger.error(f"Failed to create paypal order: {response.text}")
        return {}

@cursor
@logger_decorator
def pp_capture_order(order_uuid: str, curs: psycopg2.extensions.cursor) -> bool:
    """

    Args:
        order_uuid:
        curs:

    Returns:

    """  # TODO
    curs.execute("SELECT paypal_order_id FROM orders WHERE order_uuid = %s", (order_uuid,))
    paypal_order_id = curs.fetchone()[0]
    if pp_mode == "deployment":
        url = f"https://api-m.paypal.com/v2/checkout/orders/{paypal_order_id}/capture"
    else:
        url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{paypal_order_id}/capture"
    data = {}
    response = requests.post(url, json=data, auth=(pp_username, pp_password))
    return response.status_code == 201
