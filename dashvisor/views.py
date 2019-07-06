from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render_to_response

from dashvisor.backends import Backend


def get_backend(request):
    backend = request.session.get('backend')
    if backend is None:
        backend = Backend(request)
        backend.refresh()
        request.session.backend = backend
    return backend


def dashboard(request):
    backend = get_backend(request)
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


def control(request, server, process, action):
    backend = get_backend(request)

    if action not in ('start', 'stop', 'restart', 'tail'):
        raise Http404

    result = getattr(backend.servers[server], action)(process)
    return JsonResponse({
        'result': result
    })


def query(request):
    backend = get_backend(request)

    server_id = request.GET['server']
    server = backend.servers[server_id]
    action = request.GET['action']
    data = {'data': []}
    if action == 'refresh':
        server.refresh()
        status = server.status.values()
        status.sort(key=lambda x: (x['group'], x['name']))
        for process in status:
            process['server_name'] = "{0.name} ({0.id})".format(server)
            process['server_id'] = server_id
        data['data'].extend(status)
    if action in ('start', 'stop', 'restart'):
        program = request.GET['program']
        getattr(server, action)(program)
    return JsonResponse(data, safe=False)
