import json
from collections import OrderedDict


class BackendBase(object):
    """Backend interface"""
    def __init__(self, request=None):
        self.request = request
        self.servers = OrderedDict()

    def __call__(self, request):
        self.request = request

    def refresh(self):
        for s in self.servers.values():
            s.refresh()
