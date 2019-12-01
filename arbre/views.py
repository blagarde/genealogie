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


def get_partial(request, person_id, degree):
    neighbors_dct = utils.get_neighbors_dct()
    person_ids = set([person_id])
    for i in range(degree):
        neighbor_ids = utils.get_neighbors(neighbors_dct, person_ids)
        person_ids |= neighbor_ids
    persons = Person.objects.filter(id__in=person_ids)
    data = utils.get_data(persons)
    return JsonResponse(data)
