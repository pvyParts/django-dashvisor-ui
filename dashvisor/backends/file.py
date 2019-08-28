from django.conf import settings

from dashvisor.backends.base import BackendBase
from dashvisor.server import Server


class Backend(BackendBase):
    def __init__(self):
        super(Backend, self).__init__()
        with open(settings.DASHVISOR_CONFIG_FILE) as fp:
            for index, line in enumerate(fp.readlines()):
                sid = str(index)
                server = Server(line.strip(), id=sid)
                self.servers[sid] = server
                index += 1
