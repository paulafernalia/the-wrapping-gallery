from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.http import require_GET
from django.db.models import FloatField, Func, F, Sum, Count
from django.db.models.functions import Round
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Carry, Rating, DoneCarry, UserRating
from . import utils
from django.conf import settings
import os
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView


from .forms import CustomUserCreationForm, CustomLoginForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = "registration/login.html"
    success_url = "/"


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
    user = request.user  # Get the logged-in user

    # Get all distinct positions and sizes
    positions = Carry.objects.values_list('position', flat=True).distinct()
    sizes = Carry.objects.values_list('size', flat=True).distinct()

    # Pre-fetch all carries and group by position and size
    all_carries = Carry.objects.filter(position__in=positions, size__in=sizes).values('position', 'size').annotate(total_count=Count('name'))

    # Create a dictionary to quickly access the total counts of carries
    total_carries = {}
    for carry in all_carries:
        position = carry['position']
        size = carry['size']
        count = carry['total_count']

        if position not in total_carries:
            total_carries[position] = {}
        total_carries[position][size] = count

    # Get done carries by the user in one query
    user_done_carries = DoneCarry.objects.filter(user=user).select_related('carry')
    
    # Create structures for user carries
    done_counts = {}
    done_carry_names = {}
    
    # Initialize the structures for positions
    for position in positions:
        done_counts[position] = {}
        done_carry_names[position] = {}
        
        for size in sizes:
            # Filter user done carries by position and size
            user_done = user_done_carries.filter(carry__position=position, carry__size=size)
            
            # Done count and names of done carries
            done_counts[position][size] = user_done.count()
            done_carry_names[position][size] = list(user_done.values_list('carry__name', flat=True))  # Get carry names

    # Pass the separated carries information to the template
    context = {
        'positions': positions,
        'sizes': sizes,
        'total_carries': total_carries,
        'done_counts': done_counts,
        'done_carry_names': done_carry_names,
    }

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

    user_ratings_data = {
        "newborns": 0,
        "legstraighteners": 0,
        "leaners": 0,
        "bigkids": 0,
        "feeding": 0,
        "quickups": 0,
        "pregnancy": 0,
        "difficulty": 0,
        "fancy": 0,
    }
    
    if user.is_authenticated:
        is_done = DoneCarry.objects.filter(carry=carry, user=user).exists()
        
        # Fetch the user's rating for the carry, if it exists
        user_rating = UserRating.objects.filter(carry=carry, user=user).first()

        if user_rating:
            user_ratings_data = user_rating.to_dict()
    else:
        is_done = False        

    # Get the carry context
    carry_context = utils.get_carry_context(name)
    
    # Add 'is_done' and user ratings to the context
    context = {**carry_context, 'is_done': is_done, 'user_ratings': user_ratings_data}

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
        DoneCarry.objects.create(carry=carry, user=user)
    
    # Render the page again
    return redirect('carry', name=carry_name)


@login_required
def remove_done(request, carry_name):
    carry = get_object_or_404(Carry, name=carry_name)
    user = request.user

    # Remove from favorites if it exists
    DoneCarry.objects.filter(carry=carry, user=user).delete()

    return redirect('carry', name=carry_name)

@login_required
def get_done_carries(request):
    if request.user.is_authenticated:
        carries = DoneCarry.objects.filter(user=request.user).values_list('carry__name', flat=True)
        return JsonResponse({"carries": list(carries)})
    else:
        return JsonResponse({"error": "User not authenticated"}, status=403)


@login_required
def submit_review(request, carry_name):
    if request.method == "POST" and request.user.is_authenticated:
        # Get the rating values from the form
        user = request.user

        # Fetch the relevant carry object based on carry_name
        carry = Carry.objects.get(name=carry_name)

        # Create or update the UserRating instance
        user_rating, created = UserRating.objects.update_or_create(
            user=request.user,
            carry=carry,
            defaults={
                'newborns': request.POST.get('newborns_vote', 0),
                'legstraighteners': request.POST.get('legstraighteners_vote', 0),
                'leaners': request.POST.get('leaners_vote', 0),
                'bigkids': request.POST.get('bigkids_vote', 0),
                'feeding': request.POST.get('feeding_vote', 0),
                'quickups': request.POST.get('quickups_vote', 0),
                'difficulty': request.POST.get('difficulty_vote', 0),
                'fancy': request.POST.get('fancy_vote', 0),
            }
        )

    return redirect('carry', name=carry_name)
