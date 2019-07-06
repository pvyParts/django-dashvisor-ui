from django.conf import settings
from django.utils.module_loading import import_string


def get_backend(request=None):
    backend_path = getattr(settings, 'DASHVISOR_BACKEND',
                           'dashvisor.backends.file.Backend')
    return import_string(backend_path)(request=request)


backend = get_backend()
