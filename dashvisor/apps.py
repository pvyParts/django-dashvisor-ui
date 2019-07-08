from django.apps import AppConfig
from django.conf import settings


class DashvisorConfig(AppConfig):
    name = 'dashvisor'
    verbose_name = "Dashvisor"

    def get_option(self, name, default=None):
        return getattr(settings, self.name.upper() + "_" + name.upper(), default)
