"""Paymob Base API interface."""

import json

import requests

from core import settings as core_base_settings


class PaymobBaseAPIClient:

    def __init__(self):
        self.BASE_URL = core_base_settings.PAYMOB_BASE_URL
        self.HEADERS = {
            'Content-Type': 'application/json'
        }
        self.client_id = core_base_settings.PAYMOB_CLIENT_ID
        self.client_secret = core_base_settings.PAYMOB_CLIENT_SECRET
        self.username = core_base_settings.PAYMOB_USERNAME
        self.password = core_base_settings.PAYMOB_PASSWORD
        self.timeout = core_base_settings.TIMEOUT

    def create_request_session(self):
        session = requests.Session()
        session.headers.update(self.HEADERS)
        return session

    def login(self):
        url = f'{self.BASE_URL}o/token/'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': self.password,
            'grant_type': 'password'
        }
        response = self.create_request_session().post(url, data=json.dumps(data), headers=headers)
        return response.status_code, response.json()

    def get_access_token(self):
        statusCode, response = self.login()
        access_token = response['access_token']
        return access_token
