from django.shortcuts import render
from arbre.models import Person
from django.http import JsonResponse
from arbre import utils


def get_json(request):
    all_persons = Person.objects.all()
    data = utils.get_data(all_persons)
    return JsonResponse(data, json_dumps_params={'indent': 2})


def simpsons(request):
    return render(request, 'arbre/simpsons.html')


def arbre(request):
    return render(request, 'arbre/arbre.html')


def get_partial(request, person_id, distance):
    neighbors = utils.get_partial(person_id, distance)
    data = utils.get_data(neighbors)
    return JsonResponse(data, json_dumps_params={'indent': 2})
