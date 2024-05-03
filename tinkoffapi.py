from typing import Optional
import hashlib
import requests

URL = "https://securepay.tinkoff.ru"

def hash_data(data: dict, password: str) -> dict:
    fields = list(data.items())
    fields.append(("Password", password))
    fields.sort(key=lambda x: x[0])

    values = "".join([str(x[1]) for x in fields])
    token = hashlib.sha256(bytes(values, encoding="utf-8"))

    new_data = data.copy()
    new_data["Token"] = token.hexdigest()

    return new_data


class StandardPaymentRequest:
    def __init__(self, terminal_key, amount, order_id, description, successURL, failURL):
        self.terminal_key = terminal_key
        self.amount = amount
        self.order_id = order_id
        self.description = description
        self.successURL = successURL
        self.failURL = failURL

class StandardPaymentResponse:
    def __init__(self, success, error_code, terminal_key=None, status=None, payment_id=None, order_id=None, amount=None,paymentURL=None, message=None, details=None):
        self.success = success
        self.error_code = error_code
        self.terminal_key = terminal_key
        self.status = status
        self.payment_id = payment_id
        self.order_id = order_id
        self.amount = amount
        self.paymentURL = paymentURL
        self.message = message
        self.details = details

def init_standard(terminal_key: str, password: str, amount: int, order_id: str, description: str, success_url: str, fail_url: str) -> StandardPaymentResponse:
    request = StandardPaymentRequest(terminal_key, amount, order_id, description, success_url, fail_url)
    signed_data = hash_data(request.to_dict(), password)
    
    response = requests.post(url=f"{URL}/v2/Init", json=signed_data)
    return StandardPaymentResponse.from_dict(response.json())



class CheckPaymentRequest(self, terminal_key=None, payment_id=None):
    terminal_key: str
    payment_id: int

class CheckPaymentResponse:
    def __init__(self, success, error_code, terminal_key=None, order_id=None, payment_id=None, status=None,
                 message=None, details=None, params=None):
        self.success = success
        self.error_code = error_code
        self.terminal_key = terminal_key
        self.order_id = order_id
        self.payment_id = payment_id
        self.status = status
        self.message = message
        self.details = details
        self.params = params

def check_payment(terminal_key: str, password: str, payment_id: int) -> CheckPaymentResponse:
    request = CheckPaymentRequest(terminal_key, payment_id)
    signed_data = hash_data(request.to_dict(), password)
    
    response = requests.post(url=f"{URL}/v2/GetState", json=signed_data)
    return CheckPaymentResponse.from_dict(response.json())
