import json
import requests
from typing import Dict

from environs import Env
from psycopg2.extensions import cursor

from tools.logger_tool import logger, logger_decorator
from tools.cursor_tool import cursor as cursor_decorator

env = Env()
env.read_env()

pp_mode = env.str("PP_MODE", default="sandbox")
pp_username = env.str("PP_USERNAME")
pp_password = env.str("PP_PASSWORD")
brand_name = env.str("BRAND_NAME", default="Shop")
return_link = env.str("RETURN_LINK", default="https://google.com/")


@cursor_decorator
@logger_decorator
def pp_order_creation(order_uuid: str, curs: cursor) -> Dict[str, str]:
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
    curs.execute(
        "SELECT total FROM orders WHERE order_uuid = %s",
        (order_uuid,)
    )
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
    if (response.status_code == 200
            and json.loads(response.text)["status"] == "PAYER_ACTION_REQUIRED"):
        order_id = json.loads(response.text)["id"]
        logger.info(f"PayPal order created. Order ID: {order_id}")
        return {
            "URL": json.loads(response.text)["links"][1]["href"],
            "order_id": order_id
        }
    else:
        logger.error(f"Failed to create paypal order: {response.text}")
        return {}


@cursor_decorator
@logger_decorator
def pp_capture_order(order_uuid: str, curs: cursor) -> bool:
    """

    Args:
        order_uuid:
        curs:

    Returns:

    """  # TODO
    curs.execute(
        "SELECT paypal_order_id FROM orders WHERE order_uuid = %s",
        (order_uuid,)
    )
    paypal_order_id = curs.fetchone()[0]
    if pp_mode == "deployment":
        url = f"https://api-m.paypal.com/v2/checkout/orders/" \
              f"{paypal_order_id}/capture"
    else:
        url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/" \
              f"{paypal_order_id}/capture"
    data = {}
    response = requests.post(url, json=data, auth=(pp_username, pp_password))
    return response.status_code == 201


@cursor_decorator
@logger_decorator
def pp_rest_payout(order_uuid: str, curs: cursor) -> int:
    """

    Args:
        order_uuid:
        curs:

    Returns:

    """  # TODO
    curs.execute(
        "SELECT restaurant_uuid, dishes_subtotal FROM orders "
        "WHERE order_uuid = %s",
        (order_uuid,)
    )
    payment_info = curs.fetchone()
    rest_uuid = payment_info[0]
    to_be_paid = str(payment_info[1])
    curs.execute(
        "SELECT paypal_id FROM restaurants WHERE restaurant_uuid = %s",
        (rest_uuid,)
    )
    rest_pp_id = curs.fetchone()[0]
    if pp_mode == "deployment":
        url = f"https://api-m.paypal.com/v1/payments/payouts"
    else:
        url = f"https://api-m.sandbox.paypal.com/v1/payments/payouts"
    data = {
        "items": [
            {
                "receiver": rest_pp_id,
                "amount": {
                    "currency": "EUR",
                    "value": to_be_paid
                },
                "purpose": "GOODS"
            }
        ],
        "sender_batch_header": {
            "recipient_type": "PAYPAL_ID"
        }
    }
    response = requests.post(url, json=data, auth=(pp_username, pp_password))
    return response.status_code
