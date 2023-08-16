"""Paystack Base API interface."""

import requests

from core import settings as core_base_settings


class PaystackBaseAPIClient:

    def __init__(self):
        self.BASE_URL = core_base_settings.PAYSTACK_BASE_URL
        self.HEADERS = {
            'Authorization': f'Bearer {core_base_settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }
        self.timeout = core_base_settings.TIMEOUT

    def create_request_session(self):
        session = requests.Session()
        session.headers.update(self.HEADERS)
        return session
