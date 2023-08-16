"""
This module interfaces with Paystack Transaction API endpoint.
"""

import json

from external_apis.payments.paystack.base import PaystackBaseAPIClient


class TransactionAPIClient(PaystackBaseAPIClient):

    def transaction_base_url(self) -> str:
        return f'{self.BASE_URL}/transaction'

    def initialize_transaction(self, payload: dict):
        try:
            req = self.create_request_session()
            url = f'{self.transaction_base_url}/initialize'
            response = req.post(url, data=json.dumps(payload), timeout=self.timeout)
            return response.status_code, response.json()
        except Exception as e:  # noqa
            return 500, None

    def verify_transaction(self, reference: str):
        try:
            req = self.create_request_session()
            url = f'{self.transaction_base_url}/verify/{reference}'
            response = req.get(url, timeout=self.timeout)
            return response.status_code, response.json()
        except Exception as e:  # noqa
            return 500, None

    def charge_authorization(self, payload: dict):
        try:
            req = self.create_request_session()
            url = f'{self.transaction_base_url}/charge_authorization'
            response = req.post(url, data=json.dumps(payload), timeout=self.timeout)
            return response.status_code, response.json()
        except Exception as e:  # noqa
            return 500, None
