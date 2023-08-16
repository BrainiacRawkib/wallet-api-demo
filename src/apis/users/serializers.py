from rest_framework import serializers

from apis.users import models as user_models


class AddUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_models.User
        fields = [
            'first_name', 'last_name', 'email'
        ]

    def save(self, **kwargs):
        payload = {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'email': self.validated_data.get('email', '')
        }
        user = user_models.User.create(
            payload
        ).save()
        return user
