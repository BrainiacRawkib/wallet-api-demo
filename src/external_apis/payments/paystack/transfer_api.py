"""
This module interfaces with Paystack Transfer API endpoint.
"""

import json

from external_apis.payments.paystack.base import PaystackBaseAPIClient


class TransferAPIClient(PaystackBaseAPIClient):

    def transfer_base_url(self) -> str:
        return f'{self.BASE_URL}/transfer'

    def transfer(self, payload: dict):
        try:
            req = self.create_request_session()
            url = f'{self.transfer_base_url()}'
            payload.update({
                'source': 'balance'
            })
            response = req.post(url, data=json.dumps(payload), timeout=self.timeout)
            return response.status_code, response.json()
        except Exception:  # noqa
            return 500, None

    def finalize_transfer(self, transfer_code: str, otp: str):
        try:
            req = self.create_request_session()
            url = f'{self.transfer_base_url()}/finalize_transfer'
            data = {
                'transfer_code': transfer_code,
                'otp': otp
            }
            response = req.post(url, data=json.dumps(data), timeout=self.timeout)
            return response.status_code, response.json()
        except Exception:  # noqa
            return 500, None

    def bulk_transfer(self, transfers: list[dict]):
        try:
            req = self.create_request_session()
            url = f'{self.transfer_base_url()}/bulk'
            data = {
                'currency': 'NGN',
                'source': 'balance',
                'transfers': transfers
            }
            response = req.post(url, data=json.dumps(data), timeout=self.timeout)
            return response.status_code, response.json()
        except Exception:  # noqa
            return 500, None
