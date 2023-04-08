from django.conf import settings
from rest_framework import permissions


class ManagerIPsOnly(permissions.BasePermission):
    """
    Custom permission to allow access only from IP addresses listed in MANAGER_IPS setting.
    """

    def has_permission(self, request, view):
        # Get the MANAGER_IPS from Django settings
        manager_ips = settings.MANAGER_IPS
        # Get the client IP address from request.META
        client_ip = request.META.get('REMOTE_ADDR')

        # Validate if client IP is in MANAGER_IPS
        if client_ip not in manager_ips:
            # Return False to deny access
            return False

        # Return True to allow access
        return True
