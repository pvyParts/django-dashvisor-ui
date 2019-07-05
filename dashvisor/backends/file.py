from collections import OrderedDict

from django.conf import settings

from dashvisor.server import Server
from dashvisor.backends.base import BackendBase


class Backend(BackendBase):
    def __init__(self, request):
        super(Backend, self).__init__(request)
        fp = open(settings.DASHVISOR_CONFIG_FILE)
        index = 0
        for line in fp.xreadlines():
            id = str(index)
            server = Server(line.strip(), id=id)
            self.servers[id] = server
            index += 1
        fp.close()
