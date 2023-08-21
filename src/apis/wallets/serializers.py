from rest_framework import serializers


class WalletTransferRequestSerializer(serializers.Serializer):  # noqa
    sender_email = serializers.EmailField()
    receiver_email = serializers.EmailField()
    amount = serializers.IntegerField()
    description = serializers.CharField()


class CreateWalletSerializer(serializers.Serializer):  # noqa
    email = serializers.EmailField()
    account_name = serializers.CharField()
    account_number = serializers.CharField()
    bank_code = serializers.CharField()


class PayoutSerializer(serializers.Serializer):  # noqa
    amount = serializers.IntegerField()
    description = serializers.CharField()
    email = serializers.EmailField()


class FinalizePayoutSerializer(serializers.Serializer):  # noqa
    transfer_code = serializers.IntegerField()
    otp = serializers.IntegerField()


class PaymobTransferSerializer(serializers.Serializer):  # noqa
    email = serializers.EmailField()
    amount = serializers.IntegerField()
    issuer = serializers.CharField()
    msisdn = serializers.CharField()
