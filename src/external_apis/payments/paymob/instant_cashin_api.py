"""
This module interfaces with Paymob Instant Cashin API endpoint.
"""

import json

import requests

from external_apis.payments.paymob.base import PaymobBaseAPIClient


class InstantCashinAPIClient(PaymobBaseAPIClient):

    def instant_cahin_base_url(self) -> str:
        return f'{self.BASE_URL}/disburse/'

    def instant_cahin_headers(self) -> dict:
        access_token = self.get_access_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        return headers

    def disburse(self, payload: dict):
        try:
            url = f'{self.instant_cahin_base_url}'
            response = requests.post(url, data=json.dumps(payload), headers=self.instant_cahin_headers())
            return response.status_code, response.json()
        except Exception as e:  # noqa
            return 500, None
