from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Carry
from django.views.decorators.http import require_GET


# Create your views here.
def index(request):
    size_values = ["Any", "-5", "-4", "-3", "-2", "-1", "0", "+1", "+2"]
    position_values = ["Any", "Front", "Back"]

    return render(request, "wrappinggallery/index.html", {
        "size_values": ["Any", "-5", "-4", "-3", "-2", "-1", "0", "+1", "+2"],
        "position_values": ["Any", "Front", "Back"]
    })


def about(request):
    return render(request, "wrappinggallery/about.html")


def carry(request, name):
    # Initialize a queryset for filtering
    queryset = Carry.objects.all()
    queryset = queryset.filter(name=name)
    results = list(queryset.values('name', 'position', 'title', 'size', 'coverpicture'))

    assert len(results) == 1
    
    return render(request, "wrappinggallery/carry.html", results[0])


@require_GET
def filter_carries(request):
    # Extract lists of properties and values from GET parameters
    properties = request.GET.getlist('property[]')
    values = request.GET.getlist('value[]')

    # Initialize a queryset for filtering
    queryset = Carry.objects.all()

    # Apply filters based on properties and values
    for prop, val in zip(properties, values):
        if prop == 'size' and val != 'Any':
            queryset = queryset.filter(size=val)
        elif prop == 'position' and val != 'Any':
            queryset = queryset.filter(position=val)
        elif prop == 'partialname' and val != '':
            queryset = queryset.filter(title__icontains=val)

    # Serialize the results
    results = list(queryset.values('name', 'position', 'title', 'size', 'coverpicture'))
    return JsonResponse({'carries': results})
