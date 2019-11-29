from django.shortcuts import render
from arbre.models import Person
from django.http import JsonResponse

def arbre(request):
    all_persons = Person.objects.all()
    data = {
        'nodes': [p.as_dict() for p in all_persons],
        'edges': [{
            'child': p.id,
            'parent': parent.id
        } for p in all_persons for parent in p.parent.all()]
    }
    return JsonResponse(data)
