from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.http import require_GET
from django.db.models import FloatField, Func, F
from django.db.models.functions import Round
from .models import Carry, Ratings
from . import utils
from django.conf import settings
import os


DIFFICULTY_VALUES = ["Beginner", "Beginner+", "Intermediate", "Advanced", "Pro"]


# Create your views here.
def index(request):
    context = {}

    carry_fields = ["size", "shoulders", "layers", "position", "finish"]

    for field in carry_fields:
        idx = 0 if field in ["shoulders", "layers", "size"] else 1
        labels = [elem[idx] for elem in Carry._meta.get_field(field).choices]
        context[field + "_values"] = ["Any"] + labels

    context["shoulders_values"] = ["Varies" if x == -1 else x for x in context["shoulders_values"]]
    context["layers_values"] = ["Varies" if x == -1 else x for x in context["layers_values"]]
    context["difficulty_values"] = ["Any"] + DIFFICULTY_VALUES
    context["mmposition_values"] = [
            "Any",
            "Centred",
            "0.5 DH off centre",
            "1 DH off centre",
            "1.5 DH off centre",
            "2 DH off centre",
    ]

    return render(request, "wrappinggallery/index.html", context)

def termsandconditions(request):
    context = {}

    image_url = utils.generate_server_url("profile", "back")

    context = {"imageSrc": image_url}
    return render(request, "wrappinggallery/termsandconditions.html", context)


def about(request):
    context = {}

    image_url = utils.generate_server_url("profile", "back")

    context = {"imageSrc": image_url}
    return render(request, "wrappinggallery/about.html", context)


def downloads(request):
    context = {}

    return render(request, "wrappinggallery/downloads.html")


def faq(request):
    size_lengths = {
        1: '2.2m',
        2: '2.7m',
        3: '3.2m',
        4: '3.7m',
        5: '4.2m',
        6: '4.7m',
        7: '5.2m',
        8: '5.7m',
        9: '6.2m',
    }

    clothes_size = {
        "XS/S shirt": "size 5",
        "M/L shirt": "size 6",
        "XL/2X shirt": "size 7",
        "3X/4X shirt": 'size 8',
        "5X/6X shirt": 'size 9',
    }
    
    context = {
        'size_lengths': size_lengths,
        'clothes_size': clothes_size,
    }

    return render(request, "wrappinggallery/faq.html", context)


def steps_url(request, prefix):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        supabase = utils.initialise_supabase()
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

            batch_urls_dict = utils.generate_signed_urls(filenames, "tutorials")
            sorted_keys = sorted(batch_urls_dict.keys())
            batch_urls = [batch_urls_dict[key] for key in sorted_keys]

            signed_urls += batch_urls

            counter += 1

        return JsonResponse({"urls": signed_urls})
    else:
        # Return forbidden if not accessed by the valid request
        return HttpResponseForbidden("Access denied.")



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

    if carry_dict["videoauthor2"] == "" or carry_dict["videoauthor2"] is None:
        assert carry_dict["videotutorial2"] == "" or carry_dict["videotutorial2"] is None

        carry_dict["videoauthor2"] = "NA"
        carry_dict["videotutorial2"] = "NA"

    if carry_dict["videoauthor3"] == "" or carry_dict["videoauthor3"] is None:
        assert carry_dict["videotutorial3"] == "" or carry_dict["videotutorial3"] is None

        carry_dict["videoauthor3"] = "NA"
        carry_dict["videotutorial3"] = "NA"

    # Get image from name 
    image_url = utils.generate_server_url(name, carry_dict["position"].lower(), True)
    carry_dict["imageSrc"] = image_url

    # Add ratings
    ratingsqueryset = Ratings.objects.all()
    ratingsqueryset = ratingsqueryset.filter(carry__name=name)

    assert len(ratingsqueryset) == 1

    context = {**carry_dict, **(ratingsqueryset[0].to_dict())}

    return render(request, "wrappinggallery/carry.html", context)


def file_url(request, file_name):
    position = request.GET.get("position", "back")
    image_url = utils.generate_server_url(file_name, position)

    return JsonResponse({"url": image_url})




@require_GET
def filter_carries(request):
    # Extract lists of properties and values from GET parameters
    properties = request.GET.getlist("property[]")
    values = request.GET.getlist("value[]")
    page = int(request.GET.get("page"))
    pagesize = int(request.GET.get("page_size"))

    difficulties = dict(zip(DIFFICULTY_VALUES, [1, 2, 3, 4, 5]))

    mmpositions = {
        key: value for value, key in Carry._meta.get_field("mmposition").choices
    }

    finishes = {
        key: value for value, key in Carry._meta.get_field("finish").choices
    }

    # Initialize a queryset for filtering
    queryset = Ratings.objects.all()

    # Apply filters based on properties and values
    for prop, val in zip(properties, values): 
        if prop == "position" and val not in ["Any", "null"]:
            queryset = queryset.filter(carry__position=val.lower())
        elif prop == "shoulders" and val not in ["Any", "null"]:
            queryset = queryset.filter(carry__shoulders=val)
        elif prop == "layers" and val not in ["Any", "null", "Varies"]:
            queryset = queryset.filter(carry__layers=val)
        elif prop == "layers" and val == "Varies":
            queryset = queryset.filter(carry__layers=-1)
        elif prop == "mmposition" and val not in ["Any", "null"]:
            queryset = queryset.filter(carry__mmposition=mmpositions[val])
        elif prop == "finish" and val not in ["Any", "null"]:
            queryset = queryset.filter(carry__finish=finishes[val])
        elif prop == "partialname" and val not in ["null", ""] and val:
            queryset = queryset.filter(carry__title__icontains=val)
        elif prop == "pretied" and val == "1":
            queryset = queryset.filter(carry__pretied=val)
        elif prop == "pass_sling" and val == "1":
            queryset = queryset.filter(carry__pass_sling=val)
        elif prop == "pass_ruck" and val == "1":
            queryset = queryset.filter(carry__pass_ruck=val)
        elif prop == "pass_kangaroo" and val == "1":
            queryset = queryset.filter(carry__pass_kangaroo=val)
        elif prop == "pass_cross" and val == "1":
            queryset = queryset.filter(carry__pass_cross=val)
        elif prop == "pass_reinforcing_cross" and val == "1":
            queryset = queryset.filter(carry__pass_reinforcing_cross=val)
        elif prop == "pass_reinforcing_horizontal" and val == "1":
            queryset = queryset.filter(carry__pass_reinforcing_horizontal=val)
        elif prop == "pass_horizontal" and val == "1":
            queryset = queryset.filter(carry__pass_horizontal=val)
        elif prop == "pass_poppins" and val == "1":
            queryset = queryset.filter(carry__pass_poppins=val)
        elif prop == "no_pass_sling" and val == "1":
            queryset = queryset.filter(carry__pass_sling="0")
        elif prop == "no_pass_ruck" and val == "1":
            queryset = queryset.filter(carry__pass_ruck="0")
        elif prop == "no_pass_kangaroo" and val == "1":
            queryset = queryset.filter(carry__pass_kangaroo="0")
        elif prop == "no_pass_cross" and val == "1":
            queryset = queryset.filter(carry__pass_cross="0")
        elif prop == "no_pass_reinforcing_cross" and val == "1":
            queryset = queryset.filter(carry__pass_reinforcing_cross="0")
        elif prop == "no_pass_reinforcing_horizontal" and val == "1":
            queryset = queryset.filter(carry__pass_reinforcing_horizontal="0")
        elif prop == "no_pass_horizontal" and val == "1":
            queryset = queryset.filter(carry__pass_horizontal="0")
        elif prop == "no_pass_poppins" and val == "1":
            queryset = queryset.filter(carry__pass_poppins="0")
        elif prop == "rings" and val == "1":
            queryset = queryset.filter(carry__rings=val)
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
        elif prop == "other_chestpass" and val == "1":
            queryset = queryset.filter(carry__other_chestpass=val)
        elif prop == "other_bunchedpasses" and val == "1":
            queryset = queryset.filter(carry__other_bunchedpasses=val)
        elif prop == "other_shoulderflip" and val == "1":
            queryset = queryset.filter(carry__other_shoulderflip=val)
        elif prop == "other_twistedpass" and val == "1":
            queryset = queryset.filter(carry__other_twistedpass=val)
        elif prop == "other_waistband" and val == "1":
            queryset = queryset.filter(carry__other_waistband=val)
        elif prop == "other_legpasses" and val == "1":
            queryset = queryset.filter(carry__other_legpasses=val)
        elif prop == "other_s2s" and val == "1":
            queryset = queryset.filter(carry__other_s2s=val)
        elif prop == "other_eyelet" and val == "1":
            queryset = queryset.filter(carry__other_eyelet=val)
        elif prop == "other_poppins" and val == "1":
            queryset = queryset.filter(carry__other_poppins=val)
        elif prop == "other_sternum" and val == "1":
            queryset = queryset.filter(carry__other_sternum=val)
        elif prop == "no_other_chestpass" and val == "1":
            queryset = queryset.filter(carry__other_chestpass="0")
        elif prop == "no_other_bunchedpasses" and val == "1":
            queryset = queryset.filter(carry__other_bunchedpasses="0")
        elif prop == "no_other_shoulderflip" and val == "1":
            queryset = queryset.filter(carry__other_shoulderflip="0")
        elif prop == "no_other_twistedpass" and val == "1":
            queryset = queryset.filter(carry__other_twistedpass="0")
        elif prop == "no_other_waistband" and val == "1":
            queryset = queryset.filter(carry__other_waistband="0")
        elif prop == "no_other_legpasses" and val == "1":
            queryset = queryset.filter(carry__other_legpasses="0")
        elif prop == "no_other_s2s" and val == "1":
            queryset = queryset.filter(carry__other_s2s="0")
        elif prop == "no_other_eyelet" and val == "1":
            queryset = queryset.filter(carry__other_eyelet="0")
        elif prop == "no_other_sternum" and val == "1":
            queryset = queryset.filter(carry__other_sternum="0")
        elif prop == "no_other_poppins" and val == "1":
            queryset = queryset.filter(carry__other_poppins="0")

    sizes = request.GET.getlist("size[]", "Any")
    if sizes != ["Any"]:
        queryset = queryset.filter(carry__size__in=sizes)

    filteredDiffs = request.GET.getlist("difficulty[]", "Any")
    if filteredDiffs != ["Any"]:
        queryset = queryset.annotate(
            rounded_difficulty=Round(F("difficulty"))
        ).filter(rounded_difficulty__in=[difficulties[v] for v in filteredDiffs])

    sorted_queryset = queryset.order_by('carry__longtitle')

    start =(page - 1) * pagesize
    end = page * pagesize
    page_results = sorted_queryset[start:end]

    # Serialize the results
    results = list(
        page_results.values(
            "carry__name",
            "carry__position",
            "carry__title",
            "carry__longtitle",
            "carry__size",
            "carry__pretied",
            "carry__rings",
            "difficulty",
            "fancy",
        )
    )

    return JsonResponse({"carries": results})


def download_booklet(request, carry):
    file_path = os.path.join(settings.MEDIA_ROOT, f'{carry}_tutorial.pdf')
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f'{carry}_tutorial.pdf')
    return response

