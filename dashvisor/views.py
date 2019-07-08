from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.shortcuts import render_to_response

from dashvisor.backends import backend


def get_backend(request):
    if backend.request is None:
        backend(request)
    return backend


def dashboard(request):
    _backend = get_backend(request)
    _backend.refresh()
    return render_to_response(
        'dashvisor/dashboard.html',
        {
            'servers': _backend.servers,
            'query_url': reverse('dashvisor_query'),
            'base_path': reverse("dashvisor_dashboard"),
            'constants': {
                'stopped': 0,
                'running': 20,
            },
        }
    )


def control(request, server, process, action):
    _backend = get_backend(request)

    if action not in ('start', 'stop', 'restart', 'tail'):
        raise Http404

    result = getattr(backend.servers[server], action)(process)
    return JsonResponse({
        'result': result
    })


def query(request):
    _backend = get_backend(request)

    server_id = request.GET['server']
    server = _backend.servers[server_id]
    action = request.GET['action']
    data = {'data': []}
    if action == 'refresh':
        server.refresh()
        status = server.status.values()
        status.sort(key=lambda x: (x['group'], x['name']))
        for process in status:
            process['server'] = {
                'name': "{0.name} ({0.id})".format(server),
                'id': server_id
            }
        data['data'].extend(status)
    if action in ('start', 'stop', 'restart'):
        program = request.GET['program']
        getattr(server, action)(program)
    return JsonResponse(data, safe=False)
