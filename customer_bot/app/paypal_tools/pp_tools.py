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
    """Create PayPal order.

    Args:
        order_uuid: Order UUID.
        curs: Cursor object from psycopg2.

    Returns:
        PayPal payment link and PayPal order id.

    """
    if pp_mode == "deployment":
        url = "https://api-m.paypal.com/v2/checkout/orders"
    else:
        url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
    curs.execute("SELECT total FROM orders WHERE order_uuid = %s", (order_uuid,))
    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "EUR",
                    "value": str(curs.fetchone()[0])
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
        logger.info(f"PayPal order created. Order ID: {json.loads(response.text)["id"]}")
        return {
            "URL": json.loads(response.text)["links"][1]["href"],
            "order_id": json.loads(response.text)["id"]
        }
    else:
        logger.error(f"Failed to create paypal order: {response.text}")
        return {}


@cursor_decorator
@logger_decorator
def pp_capture_order(order_uuid: str, curs: cursor) -> bool:
    """Capture PayPal order.

    Args:
        order_uuid: Order UUID.
        curs: Cursor object from psycopg2.

    Returns:
        True if response status code is 201, False otherwise.

    """
    curs.execute("SELECT paypal_order_id FROM orders WHERE order_uuid = %s", (order_uuid,))
    if pp_mode == "deployment":
        url = f"https://api-m.paypal.com/v2/checkout/orders/{curs.fetchone()[0]}/capture"
    else:
        url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{curs.fetchone()[0]}/capture"
    data = {}
    response = requests.post(url, json=data, auth=(pp_username, pp_password))
    return response.status_code == 201


@cursor_decorator
@logger_decorator
def pp_rest_payout(order_uuid: str, curs: cursor) -> int:
    """Commit PayPal payout to the Restaurant.

    Args:
        order_uuid: Order UUID.
        curs: Cursor object from psycopg2.

    Returns:
        Response status code.

    """
    curs.execute(
        "SELECT restaurant_uuid, dishes_subtotal FROM orders WHERE order_uuid = %s", (order_uuid,)
    )
    payment_info = curs.fetchone()
    curs.execute(
        "SELECT paypal_id FROM restaurants WHERE restaurant_uuid = %s", (payment_info[0],)
    )
    if pp_mode == "deployment":
        url = f"https://api-m.paypal.com/v1/payments/payouts"
    else:
        url = f"https://api-m.sandbox.paypal.com/v1/payments/payouts"
    data = {
        "items": [
            {
                "receiver": curs.fetchone()[0],
                "amount": {
                    "currency": "EUR",
                    "value": str(payment_info[1])
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
