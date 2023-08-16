"""
the general fields to be excluded from the request payload. This function must be used when a serializer class
is a ModelSerializer class and also using the `exclude` option and not the `field` option in the `class Meta`
"""

from django.utils import timezone
from rest_framework import serializers


def base_excluded_fields(arr: list[str] = None) -> list:
    base_fields = ['date_created', 'date_updated', 'tenant_id', 'id']
    if arr:
        base_fields.extend(arr)
    return base_fields


def validate_date(value):
    if value < timezone.now():
        raise serializers.ValidationError(
            'Date cannot be a past date!'
        )
    return value
