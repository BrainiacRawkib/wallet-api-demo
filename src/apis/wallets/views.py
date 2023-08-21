from apis.base import responses as base_repo_responses, views as base_repo_views
from apis.wallets import models as wallet_models, serializers as wallet_serializers
from apis.users import models as user_models
from external_apis.payments.paymob import instant_cashin_api
from external_apis.payments.paystack import transfer_api, transfer_recipient_api


PaystackTransferAPIClient = transfer_api.TransferAPIClient()

PaystackTransferRecipientAPIClient = transfer_recipient_api.TransferRecipientAPIClient()

PaymobTransferAPIClient = instant_cashin_api.InstantCashinAPIClient()


class CreateTransferRecipientAPIView(base_repo_views.CustomGenericAPIView):

    def post(self, request, *args, **kwargs):
        try:
            serializer = wallet_serializers.CreateWalletSerializer(
                data=request.data
            )
            if serializer.is_valid():
                data = serializer.validated_data
                email = data['email']
                account_name = data['account_name']
                account_number = data['account_number']
                bank_code = data['bank_code']
                user = user_models.User.get_by_email(email)
                if not user:
                    return base_repo_responses.http_response_404(
                        'User does not exist!'
                    )
                status_code, response = PaystackTransferRecipientAPIClient.transfer_recipient(
                    account_name, account_number, bank_code
                )
                if status_code == 200:
                    recipient_code = response['data']['recipient_code']
                    wallet_payload = {
                        'user_id': user.id,
                        'transfer_recipient_code': recipient_code
                    }
                    wallet_models.Wallet.create(wallet_payload).save()
                    return base_repo_responses.http_response_200(
                        'Wallet created successfully!'
                    )
                return base_repo_responses.http_response_500(
                    self.server_error_msg
                )
            return base_repo_responses.http_response_400(
                'Bad request!', errors=serializer.errors
            )
        except Exception as e:
            self._log.error('CreateTransferRecipientAPIView.post@Error')
            self._log.error(e)
            return base_repo_responses.http_response_500(self.server_error_msg)


class TransferAPIView(base_repo_views.CustomGenericAPIView):

    def post(self, request, *args, **kwargs):
        try:
            serializer = wallet_serializers.WalletTransferRequestSerializer(
                data=request.data
            )
            if serializer.is_valid():
                data = serializer.validated_data
                sender_email = data['sender_email']
                receiver_email = data['receiver_email']
                amount = data['amount']
                description = data['description']

                sender = user_models.User.get_by_email(sender_email)
                receiver = user_models.User.get_by_email(receiver_email)

                sender_wallet = wallet_models.Wallet.get_by_user_id(sender.id)
                receiver_wallet = wallet_models.Wallet.get_by_user_id(receiver.id)

                if not sender_wallet.can_transact(int(amount)):
                    return base_repo_responses.http_response_400(
                        'Insufficient funds!'
                    )
                wallet_models.TransactionHistory.transfer(sender_wallet, receiver_wallet, amount, description)
                return base_repo_responses.http_response_200(
                    'Transaction successfully!'
                )
            return base_repo_responses.http_response_400(
                'Bad request!', errors=serializer.errors
            )
        except Exception as e:
            self._log.error('TransferAPIView.post@Error')
            self._log.error(e)
            return base_repo_responses.http_response_500(self.server_error_msg)


class PayoutAPIView(base_repo_views.CustomGenericAPIView):

    def post(self, request, *args, **kwargs):
        try:
            serializer = wallet_serializers.PayoutSerializer(
                data=request.data
            )
            if serializer.is_valid():
                data = serializer.validated_data
                email = data['email']
                amount = data['amount']
                description = data['description']

                user = user_models.User.get_by_email(email)
                if not user:
                    return base_repo_responses.http_response_404(
                        'User does not exist!'
                    )

                wallet = wallet_models.Wallet.get_by_user_id(user.id)
                if not wallet:
                    return base_repo_responses.http_response_404(
                        'Wallet does not exist!'
                    )
                transfer_payload = {
                    'reason': description,
                    'amount': amount,
                    'recipient': wallet.transfer_recipient_code
                }
                status, response = PaystackTransferAPIClient.transfer(transfer_payload)
                if status == 200:

                    return base_repo_responses.http_response_200(
                        'Payout successful!'
                    )
                return base_repo_responses.http_response_500(
                    self.server_error_msg
                )
            return base_repo_responses.http_response_400(
                'Bad request!', errors=serializer.errors
            )
        except Exception as e:
            self._log.error('PayoutAPIView.post@Error')
            self._log.error(e)
            return base_repo_responses.http_response_500(self.server_error_msg)


class FinalizePayoutAPIView(base_repo_views.CustomGenericAPIView):

    def post(self, request, *args, **kwargs):
        try:
            serializer = wallet_serializers.FinalizePayoutSerializer(
                data=request.data
            )
            if serializer.is_valid():
                data = serializer.validated_data
                transfer_code = data['transfer_code']
                otp = data['otp']
                status, response = PaystackTransferAPIClient.finalize_transfer(transfer_code, otp)
                if status == 200:
                    return base_repo_responses.http_response_200(
                        response['message']
                    )
                return base_repo_responses.http_response_400(
                    response['message']
                )
            return base_repo_responses.http_response_400(
                'Bad request!', errors=serializer.errors
            )
        except Exception as e:
            self._log.error('FinalizePayoutAPIView.post@Error')
            self._log.error(e)
            return base_repo_responses.http_response_500(self.server_error_msg)


class PaymobTransferAPIView(base_repo_views.CustomGenericAPIView):

    def post(self, request, *args, **kwargs):
        try:
            serializer = wallet_serializers.PaymobTransferSerializer(
                data=request.data
            )
            if serializer.is_valid():
                data = serializer.validated_data
                email = data['email']
                amount = data['amount']
                issuer = data['issuer']
                msisdn = data['msisdn']

                user = user_models.User.get_by_email(email)
                if not user:
                    return base_repo_responses.http_response_404(
                        'User does not exist!'
                    )

                wallet = wallet_models.Wallet.get_by_user_id(user.id)
                if not wallet:
                    return base_repo_responses.http_response_404(
                        'Wallet does not exist!'
                    )

                if not wallet.can_transact(int(amount)):
                    return base_repo_responses.http_response_400(
                        'Insufficient funds!'
                    )

                payload = {
                    'amount': amount,
                    'issuer': issuer,
                    'msisdn': msisdn
                }
                status_code, response = PaymobTransferAPIClient.disburse(payload)
                if response['disbursement_status'] == 'success':
                    wallet.deduct_balance(amount).save()
                    return base_repo_responses.http_response_200(
                        'Transfer successful!'
                    )
                return base_repo_responses.http_response_500(
                    self.server_error_msg
                )
            return base_repo_responses.http_response_400(
                'Bad request!', errors=serializer.errors
            )
        except Exception as e:
            self._log.error('PaymobTransferAPIView.post@Error')
            self._log.error(e)
            return base_repo_responses.http_response_500(self.server_error_msg)
