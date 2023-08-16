from django.urls import path, include


urlpatterns = [
    path('users/', include('apis.users.urls', namespace='users')),
    path('wallets/', include('apis.wallets.urls', namespace='wallets'))
]
