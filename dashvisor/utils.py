from django.apps import apps
from django.contrib.auth.decorators import user_passes_test

app = apps.get_app_config('dashvisor')


def login_admin_only_required(func_view):
    """Allows only administrator login"""
    return user_passes_test(lambda u: u.is_superuser,
                            login_url=app.get_option('login_url'))(func_view)
