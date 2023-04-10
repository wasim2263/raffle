from django.conf import settings
from functools import wraps
from django.http import HttpResponseForbidden


def manager_ips_only(view_func):
    """
    Decorator to allow access only from IP addresses listed in MANAGER_IPS setting.
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        manager_ips = settings.MANAGER_IPS
        client_ip = request.META.get('REMOTE_ADDR')
        print(client_ip)
        if client_ip not in manager_ips:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)

    return wrapped_view
