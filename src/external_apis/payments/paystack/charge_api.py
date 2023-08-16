"""
This module interfaces with Paystack Charge API endpoint.
"""

import json

from external_apis.payments.paystack.base import PaystackBaseAPIClient


class ChargeAPIClient(PaystackBaseAPIClient):

    def charge(self, payload: dict):
        try:
            req = self.create_request_session()
            url = f'{self.BASE_URL}/charge'
            response = req.post(url, data=json.dumps(payload))
            return response.status_code, response.json()
        except Exception as e:  # noqa
            return 500, None

    def check_charge(self, reference: str):
        try:
            req = self.create_request_session()
            url = f'{self.BASE_URL}/charge/{reference}'
            response = req.get(url)
            return response.status_code, response.json()
        except Exception as e:  # noqa
            return 500, None
