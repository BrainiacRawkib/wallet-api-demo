from apis.base import responses as base_repo_responses, views as base_repo_views
from apis.users import serializers as user_serializers


class AddUserAPIView(base_repo_views.CustomGenericAPIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        try:
            seriazlier = user_serializers.AddUserSerializer(
                data=request.data
            )
            if seriazlier.is_valid():
                seriazlier.save()
                return base_repo_responses.http_response_200(
                    'User created successfully!'
                )
            return base_repo_responses.http_response_400(
                'Bad request!', errors=seriazlier.errors
            )
        except Exception as e:
            self._log.error(e)
            self._log.error('AddUserAPIView.post@Error')
            return base_repo_responses.http_response_500(self.server_error_msg)
