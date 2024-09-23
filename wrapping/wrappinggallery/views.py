from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.http import require_GET
from django.db.models import FloatField, Func, F
from django.db.models.functions import Round
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Carry, Rating, DoneCarry
from . import utils
from django.conf import settings
import os

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


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
    image_url = utils.generate_server_url("profile", "back")

    context = {"imageSrc": image_url}
    return render(request, "wrappinggallery/termsandconditions.html", context)


def about(request):
    image_url = utils.generate_server_url("profile", "back")

    context = {"imageSrc": image_url}
    return render(request, "wrappinggallery/about.html", context)


def downloads(request):

    return render(request, "wrappinggallery/downloads.html")


def collection(request):
    sizes = range(-5, 3)  # Generates sizes from -5 to 2
    positions = ["front", "back", "tandem"]

    context = {"sizes": sizes, "positions": positions}

    return render(request, "wrappinggallery/collection.html", context)


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
    carry = get_object_or_404(Carry, name=name)
    user = request.user
    
    # Check if the carry is already marked as done (exists in the FavouriteCarry table)
    is_done = DoneCarry.objects.filter(carry=carry, user=user).exists()
    
    # Get the carry context
    carry_context = utils.get_carry_context(name)
    
    # Add 'is_done' to the context
    context = {**carry_context, 'is_done': is_done}

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
    queryset = Rating.objects.all()

    # Apply filters based on properties and values
    queryset = utils.apply_filters(
        queryset, properties, values, mmpositions, finishes, difficulties
    )

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


@login_required
def mark_as_done(request, carry_name):
    carry = get_object_or_404(Carry, name=carry_name)
    user = request.user
    
    # Check if the done already entry exists
    if not DoneCarry.objects.filter(carry=carry, user=user).exists():
        print("ADDED!")
        DoneCarry.objects.create(carry=carry, user=user)
    else:
        print("already exists")
    
    # Render the page again
    return redirect('carry', name=carry_name)


@login_required
def remove_done(request, carry_name):
    carry = get_object_or_404(Carry, name=carry_name)
    user = request.user

    # Remove from favorites if it exists
    DoneCarry.objects.filter(carry=carry, user=user).delete()

    return redirect('carry', name=carry_name)


def get_done_carries(request):
    if request.user.is_authenticated:
        carries = DoneCarry.objects.filter(user=request.user).values_list('carry__name', flat=True)
        return JsonResponse({"carries": list(carries)})
    else:
        return JsonResponse({"error": "User not authenticated"}, status=403)
