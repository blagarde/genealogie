from django.shortcuts import render
from tree.models import Person
from django.http import JsonResponse
from tree import utils


def get_json(request):
    all_persons = Person.objects.all()
    data = utils.get_data(all_persons)
    return JsonResponse(data, json_dumps_params={'indent': 2})


def simpsons(request):
    return render(request, 'tree/simpsons.html')


def tree(request, chart_type='descendants', person_id=1, distance=3):
    assert chart_type in ('descendants', 'ancestors', 'timeline')
    js_filename = ('timeline' if chart_type == 'timeline' else 'radial_tree')
    method = 'get_' + ('json' if chart_type == 'timeline' else chart_type)
    json_url = '/{m}/{p}/{d}'.format(m=method, p=person_id, d=distance)
    context = {
        'js_path': '/static/tree/js/{fn}.js'.format(fn=js_filename),
        'json_url': json_url
    }
    return render(request, 'tree/tree.html', context)


def get_partial(request, person_id, distance):
    neighbors = utils.get_partial(person_id, distance)
    data = utils.get_data(neighbors)
    return JsonResponse(data, json_dumps_params={'indent': 2})


def get_descendants(request, person_id, distance):
    data = utils.get_descendants(person_id, distance)
    return JsonResponse(data, json_dumps_params={'indent': 2})


def get_ancestors(request, person_id, distance):
    data = utils.get_ancestors(person_id, distance)
    return JsonResponse(data, json_dumps_params={'indent': 2})
