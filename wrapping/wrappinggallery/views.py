from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import FloatField, Func, F
from django.db.models.functions import Round
from .models import Carry, Ratings
from .utils import generate_signed_url


DIFFICULTY_VALUES = ["Beginner", "Beginner+", "Intermediate", "Advanced", "Pro"]


# Create your views here.
def index(request):
    context = {}

    carry_fields = ["size", "shoulders", "layers", "mmposition", "position", "finish"]

    for field in carry_fields:
        idx = 0 if field == "size" else 1
        labels = [elem[idx] for elem in Carry._meta.get_field(field).choices]
        context[field + "_values"] = ["Any"] + labels

    context["difficulty_values"] = ["Any"] + DIFFICULTY_VALUES

    return render(request, "wrappinggallery/index.html", context)


def about(request):
    context = {"imageSrc": generate_signed_url("profile.png", "misc")}
    print("context", context)
    return render(request, "wrappinggallery/about.html", context)


def carry(request, name):
    # Initialize a queryset for filtering
    queryset = Carry.objects.all()
    queryset = queryset.filter(name=name)

    assert len(queryset) == 1

    carry_dict = queryset[0].to_dict()

    if carry_dict["coverpicture"] == "" or carry_dict["coverpicture"] is None:
        if carry_dict["position"] == "Back":
            carry_dict["coverpicture"] = "placeholder_back.png"
        else:
            carry_dict["coverpicture"] = "placeholder_front.png"

    if carry_dict["videoauthor"] == "" or carry_dict["videoauthor"] is None:
        assert carry_dict["videotutorial"] == "" or carry_dict["videotutorial"] is None

        carry_dict["videoauthor"] = "NA"
        carry_dict["videotutorial"] = "NA"

    carry_dict["imageSrc"] = generate_signed_url(carry_dict["coverpicture"])

    # Add ratings
    ratingsqueryset = Ratings.objects.all()
    ratingsqueryset = ratingsqueryset.filter(carry__name=name)

    assert len(ratingsqueryset) == 1

    context = {**carry_dict, **(ratingsqueryset[0].to_dict())}

    return render(request, "wrappinggallery/carry.html", context)


def file_url(request, file_name):
    signed_url = generate_signed_url(f"{file_name}")
    if signed_url:
        return JsonResponse({"url": signed_url})
    else:
        return JsonResponse({"error": "Unable to generate signed URL"}, status=500)


@require_GET
def filter_carries(request):
    # Extract lists of properties and values from GET parameters
    properties = request.GET.getlist("property[]")
    values = request.GET.getlist("value[]")

    difficulties = dict(zip(DIFFICULTY_VALUES, [1, 2, 3, 4, 5]))

    # Initialize a queryset for filtering
    queryset = Ratings.objects.all()

    # Apply filters based on properties and values
    for prop, val in zip(properties, values):
        if prop == "size" and val != "Any":
            queryset = queryset.filter(carry__size=val)
        elif prop == "position" and val != "Any":
            queryset = queryset.filter(carry__position=val)
        elif prop == "finish" and val != "Any":
            queryset = queryset.filter(carry__finish=val)
        elif prop == "partialname" and val != "":
            queryset = queryset.filter(carry__title__icontains=val)
        elif prop == "difficulty" and val != "Any":
            queryset = queryset.annotate(
                rounded_difficulty=Round(F("difficulty"))
            ).filter(rounded_difficulty=difficulties[val])
        elif prop == "pretied" and val != "null":
            queryset = queryset.filter(carry__pretied=val)

    # Extract start and end parameters
    start = int(request.GET.get("start", 0))
    end = int(request.GET.get("end", 8)) + 1  # end is inclusive

    # Get the total count of items
    total_count = queryset.count()

    # Ensure that start and end are within the bounds
    if start < 0:
        start = 0
    if end > total_count:
        end = total_count

    # Apply pagination
    print("getting results", start, end)
    queryset = queryset[start:end]

    # Serialize the results
    results = list(
        queryset.values(
            "carry__name",
            "carry__position",
            "carry__title",
            "carry__size",
            "carry__coverpicture",
            "carry__pretied",
            "difficulty",
            "fancy",
        )
    )

    return JsonResponse({"carries": results})
