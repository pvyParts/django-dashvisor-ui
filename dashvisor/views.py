from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.shortcuts import render_to_response

from dashvisor import backends
from dashvisor.utils import login_admin_only_required


def get_backend(request):
    if backends.backend.request is None:
        backends.backend(request)
    return backends.backend


@login_admin_only_required
def dashboard(request):
    backend = get_backend(request)
    backend.refresh()
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


@login_admin_only_required
def control(request, server, process, action):
    _backend = get_backend(request)

    if action not in ('start', 'stop', 'restart', 'tail',
                      'start_all', 'restart_all', 'stop_all'):
        raise Http404
    if server == '*':
        result = []
        for server in backend.servers:
            result.append(getattr(backend.servers[server], action)())
    else:
        result = getattr(backend.servers[server], action)(process)
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
    backend = get_backend(request)
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
