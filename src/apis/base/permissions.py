from rest_framework import permissions


class CustomBasePermission(permissions.BasePermission):

    def get_groups_permissions(self, request, action_value: str) -> bool:
        pass
