from decimal import Decimal
from uuid import uuid4

from django.db import models


class Wallet(models.Model):
    id = models.CharField(primary_key=True, default=f'wal_{uuid4().hex}', max_length=100)
    user_id = models.CharField(max_length=100, default="")
    transfer_recipient_code = models.CharField(max_length=100, default="")
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def add_balance(self, amount: int | Decimal):
        self.balance += amount
        return self

    def deduct_balance(self, amount: int | Decimal):
        self.balance -= amount
        return self

    def can_transact(self, amount: int | Decimal) -> bool:
        return self.balance > amount

    @staticmethod
    def create(payload: dict):
        return Wallet(
            user_id=payload.get('user_id', ''),
            transfer_recipient_code=payload.get('transfer_recipient_code', '')
        )

    @staticmethod
    def get_by_id(id: str):  # noqa
        try:
            return Wallet.objects.get(id=id)
        except (Exception, Wallet.DoesNotExist):
            return None

    @staticmethod
    def get_by_user_id(user_id: str):
        try:
            return Wallet.objects.get(user_id=user_id)
        except (Exception, Wallet.DoesNotExist):
            return None


class TransactionHistory(models.Model):
    id = models.CharField(primary_key=True, default=uuid4().hex, max_length=100)
    source_wallet_id = models.CharField(max_length=80, default="")
    receiver_wallet_id = models.CharField(max_length=80, default="")
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    new_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    old_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    description = models.CharField(max_length=100, default="")

    @staticmethod
    def transfer(source_wallet: Wallet, receiver_wallet: Wallet, amount: int | Decimal, description: str):
        source_wallet_old_balance = source_wallet.balance
        receiver_wallet_old_balance = receiver_wallet.balance

        source_wallet.deduct_balance(amount)
        receiver_wallet.add_balance(amount)

        source_wallet_new_balance = source_wallet.balance
        receiver_wallet_new_balance = receiver_wallet.balance

        # save
        source_wallet.save()
        receiver_wallet.save()

        source_wallet_payload = {
            'source_wallet_id': source_wallet.id,
            'receiver_wallet_id': receiver_wallet.id,
            'amount': amount,
            'new_balance': source_wallet_new_balance,
            'old_balance': source_wallet_old_balance,
            'description': description
        }

        receiver_wallet_payload = {
            'source_wallet_id': source_wallet.id,
            'receiver_wallet_id': receiver_wallet.id,
            'amount': amount,
            'new_balance': receiver_wallet_new_balance,
            'old_balance': receiver_wallet_old_balance,
            'description': description
        }

        source_transaction = TransactionHistory.create(source_wallet_payload).save()

        receiver_transaction = TransactionHistory.create(receiver_wallet_payload).save()
        return source_transaction, receiver_transaction

    @staticmethod
    def create(payload: dict):
        return TransactionHistory(
            source_wallet_id=payload.get('source_wallet_id', ''),
            receiver_wallet_id=payload.get('receiver_wallet_id', ''),
            amount=payload.get('amount', 0),
            new_balance=payload.get('new_balance', 0),
            old_balance=payload.get('old_balance', 0),
            description=payload.get('description', '')
        )


class TransferCode(models.Model):
    id = models.CharField(primary_key=True, default=f'trf_code_{uuid4().hex}', max_length=100)
    transfer_code = models.CharField(max_length=100, default="")
    wallet_id = models.CharField(max_length=100, default="")

    @staticmethod
    def create(payload: dict):
        return TransferCode(
            transfer_code=payload.get('transfer_code', ''),
            wallet_id=payload.get('wallet_id', '')
        )

    @staticmethod
    def get_by_transfer_code(code: str):
        try:
            return TransferCode.objects.get(transfer_code=code)
        except (Exception, TransferCode.DoesNotExist):
            return None
