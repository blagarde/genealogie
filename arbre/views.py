from django.shortcuts import render
from arbre.models import Person
from django.http import JsonResponse
from arbre import utils


def get_json(request):
    all_persons = Person.objects.all()
    data = utils.get_data(all_persons)
    return JsonResponse(data)


def simpsons(request):
    return render(request, 'arbre/simpsons.html')


def arbre(request):
    return render(request, 'arbre/arbre.html')


def get_partial(request, person_id, distance):
    neighbors_dct = utils.get_neighbors_dct()
    distance_dct = {person_id: 0}
    for i in range(distance):
        person_ids_seen = distance_dct.keys()
        neighbor_ids = utils.get_neighbors(neighbors_dct, person_ids_seen)
        for neighbor_id in neighbor_ids.difference(person_ids_seen):
            distance_dct[neighbor_id] = i + 1
    persons = Person.objects.filter(id__in=person_ids_seen)
    data = utils.get_data(persons)
    return JsonResponse(data)
