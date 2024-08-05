from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import FloatField, Func, F
from django.db.models.functions import Round
from .models import Carry, Ratings
from .utils import generate_signed_url, generate_signed_urls, initialise_supabase
from django.conf import settings


DIFFICULTY_VALUES = ["Beginner", "Beginner+", "Intermediate", "Advanced", "Pro"]


# Create your views here.
def index(request):
    context = {}

    carry_fields = ["size", "shoulders", "layers", "mmposition", "position", "finish"]

    for field in carry_fields:
        idx = 0 if field in ["shoulders", "layers", "size"] else 1
        labels = [elem[idx] for elem in Carry._meta.get_field(field).choices]
        context[field + "_values"] = ["Any"] + labels

    context["difficulty_values"] = ["Any"] + DIFFICULTY_VALUES

    return render(request, "wrappinggallery/index.html", context)


def about(request):
    context = {}

    if settings.SUPABASE_URL == "https://default.supabase.co":
        file_name = "profile.png"
        context = {"imageSrc": settings.MEDIA_URL + file_name}
    else:
        context = {"imageSrc": generate_signed_url(
            "profile.png",
            settings.SUPABASE_MISC_BUCKET
        )}
    return render(request, "wrappinggallery/about.html", context)


def steps_url(request, prefix):
    supabase = initialise_supabase()
    bucketname = settings.SUPABASE_TUTORIAL_BUCKET

    batchsize = 10
    signed_urls = []
    counter = 0
    batch_urls = ["dummy"]

    while len(batch_urls) != 0:
        filenames = []
        range_start = counter * batchsize
        range_end = (counter + 1) * batchsize
        
        for i in [f"{i+1:02}" for i in range(range_start, range_end)]:
            filenames.append(f"{prefix}_step{i}.png")

        batch_urls_dict = generate_signed_urls(filenames, "tutorials")
        sorted_keys = sorted(batch_urls_dict.keys())
        batch_urls = [batch_urls_dict[key] for key in sorted_keys]

        signed_urls += batch_urls

        counter += 1

    return JsonResponse({"urls": signed_urls})



def carry(request, name):
    # Initialize a queryset for filtering
    queryset = Carry.objects.all()
    queryset = queryset.filter(name=name)

    assert len(queryset) == 1

    carry_dict = queryset[0].to_dict()

    if carry_dict["videoauthor"] == "" or carry_dict["videoauthor"] is None:
        assert carry_dict["videotutorial"] == "" or carry_dict["videotutorial"] is None

        carry_dict["videoauthor"] = "NA"
        carry_dict["videotutorial"] = "NA"

    # Try to get image from name 
    bucket = settings.SUPABASE_COVER_BUCKET
    image_url = generate_signed_url(f"{name}.png", bucket)
    if image_url is None:
        if carry_dict["position"] == "Back":
            placeholder = "placeholder_back.png"
        else:
            placeholder = "placeholder_front.png"

        # Get url of placeholder
        image_url = generate_signed_url(placeholder, bucket)

    carry_dict["imageSrc"] = image_url

    # Add ratings
    ratingsqueryset = Ratings.objects.all()
    ratingsqueryset = ratingsqueryset.filter(carry__name=name)

    assert len(ratingsqueryset) == 1

    context = {**carry_dict, **(ratingsqueryset[0].to_dict())}

    return render(request, "wrappinggallery/carry.html", context)


def file_url(request, file_name):
    bucket_name = request.GET.get('bucket')

    # if no access to S3 storage:
    if settings.SUPABASE_URL == "https://default.supabase.co":
        print("WARNING: missing connection details for S3 bucket in SUPABASE, using default image in media folder")
        file_name = "placeholder_back.png"
        return JsonResponse({"url": settings.MEDIA_URL + file_name})


    signed_url = generate_signed_url(file_name, bucket_name)
    if signed_url:
        return JsonResponse({"url": signed_url})
    else:
        return JsonResponse({"empty": None})


@require_GET
def filter_carries(request):
    # Extract lists of properties and values from GET parameters
    properties = request.GET.getlist("property[]")
    values = request.GET.getlist("value[]")

    difficulties = dict(zip(DIFFICULTY_VALUES, [1, 2, 3, 4, 5]))

    mmpositions = {
        key: value for value, key in Carry._meta.get_field("mmposition").choices
    }

    # Initialize a queryset for filtering
    queryset = Ratings.objects.all()

    # Apply filters based on properties and values
    for prop, val in zip(properties, values):
        if prop == "size" and val != "Any":
            queryset = queryset.filter(carry__size=val)
        elif prop == "position" and val != "Any":
            queryset = queryset.filter(carry__position=val.lower())
        elif prop == "shoulders" and val != "Any":
            queryset = queryset.filter(carry__shoulders=val)
        elif prop == "layers" and val != "Any":
            queryset = queryset.filter(carry__layers=val)
        elif prop == "mmposition" and val != "Any":
            queryset = queryset.filter(carry__mmposition=mmpositions[val])
        elif prop == "finish" and val != "Any":
            queryset = queryset.filter(carry__finish=val)
        elif prop == "partialname" and val not in ["null", ""] and val:
            queryset = queryset.filter(carry__title__icontains=val)
        elif prop == "difficulty" and val != "Any":
            queryset = queryset.annotate(
                rounded_difficulty=Round(F("difficulty"))
            ).filter(rounded_difficulty=difficulties[val])
        elif prop == "pretied" and val != "null":
            queryset = queryset.filter(carry__pretied=val)
        elif prop == "newborns" and val == "1":
            queryset = queryset.filter(newborns__gte=3.5)
        elif prop == "legstraighteners" and val == "1":
            queryset = queryset.filter(legstraighteners__gte=3.5)
        elif prop == "leaners" and val == "1":
            queryset = queryset.filter(leaners__gte=3.5)
        elif prop == "bigkids" and val == "1":
            queryset = queryset.filter(bigkids__gte=3.5)
        elif prop == "feeding" and val == "1":
            queryset = queryset.filter(feeding__gte=3.5)
        elif prop == "quickups" and val == "1":
            queryset = queryset.filter(quickups__gte=3.5)
        elif prop == "fancy" and val == "1":
            queryset = queryset.filter(fancy__gte=3.5)

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

    sorted_queryset = queryset.order_by('carry__title')

    # Apply pagination
    sorted_queryset = sorted_queryset[start:end]

    # Serialize the results
    results = list(
        sorted_queryset.values(
            "carry__name",
            "carry__position",
            "carry__title",
            "carry__size",
            "carry__pretied",
            "difficulty",
            "fancy",
        )
    )

    return JsonResponse({"carries": results})
