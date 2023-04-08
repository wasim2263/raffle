from django.conf import settings
from functools import wraps
from django.http import HttpResponseForbidden

def manager_ips_only(view_func):
    """
    Decorator to allow access only from IP addresses listed in MANAGER_IPS setting.
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Get the MANAGER_IPS from Django settings
        manager_ips = settings.MANAGER_IPS

        # Get the client IP address from request.META
        client_ip = request.META.get('REMOTE_ADDR')

        # Validate if client IP is in MANAGER_IPS
        if client_ip not in manager_ips:
            # Return HTTP 403 Forbidden response
            return HttpResponseForbidden()

        # Call the view function
        return view_func(request, *args, **kwargs)

    return wrapped_view
