from django.urls import path

from apis.wallets import views as wallet_views


app_name = "wallets"

urlpatterns = [
    path(
        'create-transfer-recipient',
        wallet_views.CreateTransferRecipientAPIView.as_view(),
        name='create-transfer-recipient'
    ),
    path(
        'transfer',
        wallet_views.TransferAPIView.as_view(),
        name='transfer'
    ),
    path(
        'payout',
        wallet_views.PayoutAPIView.as_view(),
        name='payout'
    ),
    path(
        'finalize-payout',
        wallet_views.FinalizePayoutAPIView.as_view(),
        name='finalize-payout'
    ),
    path(
        'payout-with-paymob',
        wallet_views.PaymobTransferAPIView.as_view(),
        name='payout-with-paymob'
    )
]
