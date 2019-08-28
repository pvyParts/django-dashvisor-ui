import socket

from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.shortcuts import render_to_response

from dashvisor.backends import backend
from dashvisor.utils import login_admin_only_required


@login_admin_only_required
def dashboard(request):
    try:
        backend.refresh()
    except socket.error:
        pass
    return render_to_response(
        'dashvisor/dashboard.html',
        {
            'servers': backend.servers,
            'query_url': reverse('dashvisor_query'),
            'base_path': reverse("dashvisor_dashboard"),
            'constants': {
                'stopped': 0,
                'running': 20,
            },
        }
    )


class ControlAction(list):
    def __init__(self):
        super(ControlAction, self).__init__()
        self.extend([
            'start',
            'stop',
            'restart',
            'tail',
            'start_all',
            'restart_all',
            'stop_all',
            'reload_config'
        ])

    def check_perm_or_404(self, action):
        if action not in self:
            raise Http404


@login_admin_only_required
def control(request, server_alias, process, action):
    request_method = getattr(request, request.method)
    ControlAction().check_perm_or_404(action)
    action_kwargs = {}
    attrs = {'offset': int, 'length': int}
    for name in attrs:
        if name in request_method:
            action_kwargs[name] = attrs[name](request_method[name])
    action_args = []
    if process != '*':
        action_args.append(process)
    if server_alias == '*':
        result = []
        for server_alias in backend.servers:
            server = backend.servers[server_alias]
            func = getattr(server, action)
            result.append(func(*action_args, **action_kwargs))
    else:
        func = getattr(backend.servers[server_alias], action)
        result = func(*action_args, **action_kwargs)
    return JsonResponse({
        'result': result,
    }, safe=False)


def _get_server_status(request, server, action):
    """get server status data"""
    if action == 'refresh':
        server.refresh()
    status = server.status.values()
    status.sort(key=lambda x: (x['group'], x['name']))
    for process in status:
        process['server'] = {
            'name': "{0.name} ({0.id})".format(server),
            'id': server.id
        }
    return status


@login_admin_only_required
def query(request):
    server_alias = request.GET.get('server_alias', '*')
    action = request.GET.get('action')
    data = {'data': []}
    if server_alias == "*":
        for server in backend.servers.itervalues():
            status = _get_server_status(request, server, action)
            data['data'].extend(status)
    else:
        server = backend.servers[server_alias]
        status = _get_server_status(request, server, action)
        data['data'].extend(status)
    return JsonResponse(data, safe=False)
