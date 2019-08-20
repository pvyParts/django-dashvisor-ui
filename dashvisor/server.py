from collections import OrderedDict
from httplib import CannotSendRequest
from urlparse import urlparse
from xmlrpclib import ServerProxy, Fault


class ExceptionHandler(object):
    def __init__(self, exc, defaults=None):
        self.exc = exc
        if defaults is None:
            defaults = False
        self.defaults = defaults

    def __call__(self, method):
        def wrap(self_, *args_, **kwargs_):
            try:
                return method(self_, *args_, **kwargs_)
            except self.exc:
                return self.defaults

        return wrap


class Server(object):
    def __init__(self, connection_string, id):
        self.name = urlparse(connection_string).hostname
        self.connection = ServerProxy(connection_string)
        self.status = OrderedDict()
        self.id = id

    @ExceptionHandler(CannotSendRequest)
    def refresh(self):
        self.status = OrderedDict(("%s:%s" % (i['group'], i['name']), i)
                                  for i in self.connection.supervisor.getAllProcessInfo())
        for key, program in self.status.items():
            program['id'] = key
            program['human_name'] = program['name']
            if program['name'] != program['group']:
                program['human_name'] = "%s:%s" % (program['group'], program['name'])

    @ExceptionHandler(CannotSendRequest)
    def stop(self, name):
        try:
            return self.connection.supervisor.stopProcess(name)
        except Fault as e:
            if e.faultString.startswith('NOT_RUNNING'):
                return False
            raise

    @ExceptionHandler(CannotSendRequest, defaults={'content': '', 'size': 0,
                                                   'overflow': False})
    def tail(self, name, offset=-1, length=None):
        if length is None:
            length = 1024 * 5
        try:
            result = self.connection.supervisor.tailProcessLog(name, offset, length)
            return dict(zip(('content', 'size', 'overflow'), result))
        except Fault as e:
            raise

    @ExceptionHandler(CannotSendRequest)
    def start(self, name):
        try:
            return self.connection.supervisor.startProcess(name)
        except Fault as e:
            if e.faultString.startswith('ALREADY_STARTED'):
                return False
            raise

    def start_all(self):
        return self.connection.supervisor.startAllProcesses()

    def restart_all(self):
        self.stop_all()
        return self.start_all()

    def stop_all(self):
        return self.connection.supervisor.stopAllProcesses()

    def restart(self, name):
        self.stop(name)
        return self.start(name)
