from django.urls import path

from apis.users import views as user_views


app_name = "users"

urlpatterns = [
    path(
        'add',
        user_views.AddUserAPIView.as_view(),
        name='add'
    )
]
