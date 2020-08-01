from rest_framework.permissions import BasePermission

from django.conf import settings


class CheckSecretAPI(BasePermission):
    message = 'Correct SECRET header was not provided.'

    def has_permission(self, request, view):
        api_key_secret = request.META.get('HTTP_SECRET', None)
        return api_key_secret and api_key_secret == settings.API_KEY_SECRET
