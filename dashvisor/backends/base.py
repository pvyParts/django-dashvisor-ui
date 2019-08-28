import json
from collections import OrderedDict


class BackendBase(object):
    """Backend interface"""
    def __init__(self):
        self.servers = OrderedDict()

    def refresh(self):
        for s in self.servers.values():
            s.refresh()
