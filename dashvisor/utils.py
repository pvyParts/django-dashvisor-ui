from django.apps import apps
from django.contrib.auth.decorators import user_passes_test
from django.utils.module_loading import import_string
from django.utils.six import string_types

app = apps.get_app_config('dashvisor')

_func_test = app.get_option('user_passes_test',
                            lambda u: u.is_superuser)
if isinstance(_func_test, string_types):
    _func_test = import_string(_func_test)

_login_url = app.get_option('login_url')


def login_admin_only_required(func_view):
    """Allows only administrator login"""
    return user_passes_test(_func_test, login_url=_login_url)(func_view)
