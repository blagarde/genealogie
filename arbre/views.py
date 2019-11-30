from django.shortcuts import render
from arbre.models import Person
from django.http import JsonResponse


def get_json(request):
    all_persons = Person.objects.all()
    data = {
        'nodes': [p.as_dict() for p in all_persons],
        'edges': [{
            'source': p.id,
            'target': parent.id
        } for p in all_persons for parent in p.parent.all()]
    }
    return JsonResponse(data)


def simpsons(request):
    return render(request, 'arbre/simpsons.html')
