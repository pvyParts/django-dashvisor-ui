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
            'constants': {
                'stopped': 0,
                'running': 20,
            },
        }
    )


def control(request, server, process, action):
    backend = get_backend(request)

    if action not in ('start', 'stop', 'restart'):
        raise Http404

    getattr(backend.servers[server], action)(process)
    return HttpResponseRedirect(reverse('dashvisor_dashboard'))


def query(request):
    backend = get_backend(request)

    server_id = request.GET['server']
    server = backend.servers[server_id]
    action = request.GET['action']
    response_dict = {}
    if action == 'refresh':
        server.refresh()
        response_dict['status'] = server.status.values()
        response_dict['status'].sort(key=lambda x: (x['group'], x['name']))
        response_dict['server'] = {'name': server.name, 'id': server_id}
    if action in ('start', 'stop', 'restart'):
        program = request.GET['program']
        getattr(server, action)(program)

    return JsonResponse(response_dict)
