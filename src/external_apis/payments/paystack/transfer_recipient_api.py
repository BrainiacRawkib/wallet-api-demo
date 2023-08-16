"""
This module interfaces with Paystack TransferRecipient API endpoint.
"""

import json

from external_apis.payments.paystack.base import PaystackBaseAPIClient


class TransferRecipientAPIClient(PaystackBaseAPIClient):

    def transfer_recipient(self, name: str, account_number: str, bank_code: str):
        try:
            req = self.create_request_session()
            url = f'{self.BASE_URL}/transferrecipient'
            data = {
                'type': 'nuban',
                'name': name,
                'account_number': account_number,
                'bank_code': bank_code,
                'currency': 'NGN'
            }
            response = req.post(url, data=json.dumps(data), timeout=self.timeout)
            return response.status_code, response.json()
        except Exceptio:  # noqa
            return 500, None
