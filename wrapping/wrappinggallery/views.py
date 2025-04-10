from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.http import require_GET, require_POST
from django.db.models import FloatField, Func, F, Sum, Count, Q
from django.db.models.functions import Round
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Carry, Rating, DoneCarry, UserRating, Achievement, UserAchievement, TodoCarry
from . import utils
from django.conf import settings
import os
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render

from django.db.models import Case, When, BooleanField
import json
from .forms import CustomUserCreationForm, CustomLoginForm, UserUpdateForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = "registration/login.html"
    success_url = "/"


def account_deleted(request):
    return render(request, 'registration/account_deleted.html')



def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow:",
        "Sitemap: https://thewrappinggallery.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@login_required
def profile_view(request):
    messages.get_messages(request).used = True  # This will clear out all messages
    
    user = request.user
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)

    return render(request, 'registration/profile.html', {'user_form': user_form})

@login_required
def delete_account(request):
    messages.get_messages(request).used = True  # This will clear out all messages
    
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('account_deleted')

    return render(request, 'registration/delete_account.html', {'user': user})


DIFFICULTY_VALUES = ["Beginner", "Beginner+", "Intermediate", "Advanced", "Pro"]

@login_required
def achievements(request):
    # Get all achievements
    all_achievements = Achievement.objects.all()

    # Get achievements unlocked by the current user
    user_achievements = UserAchievement.objects.filter(user=request.user).values_list('achievement__name', flat=True)

    # Prepare the context with combined data
    achievements_data = []
    for achievement in all_achievements:
        achievements_data.append({
            'name': achievement.name,
            'title': achievement.title,
            'description': achievement.description,
            'category': achievement.category,
            'completed': achievement.name in user_achievements,
        })

    category_choices = Achievement.CATEGORY_CHOICES

    # Pass combined data to context
    context = {
        'achievements': achievements_data,
        'category_choices': category_choices,
    }

    return render(request, "wrappinggallery/achievements.html", context)


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

    # Convert the QuerySet to a list of dictionaries
    context["carries"] = list(
        Carry.objects.values('name', 'longtitle', 'title').order_by('longtitle')
    )

    return render(request, "wrappinggallery/index.html", context)

def termsandconditions(request):
    image_url = utils.generate_carry_url("profile", "back")

    context = {"imageSrc": image_url}
    return render(request, "wrappinggallery/termsandconditions.html", context)


def about(request):
    image_url = utils.generate_carry_url("profile", "back")
    return render(request, "wrappinggallery/about.html",  {"imageSrc": image_url})


def downloads(request):
    return render(request, "wrappinggallery/downloads.html")

@login_required
def collection(request):
    user = request.user  # Get the logged-in user

    # Get all distinct positions and sizes
    positions = Carry.objects.values_list('position', flat=True).distinct().order_by('position')
    sizes = Carry.objects.values_list('size', flat=True).distinct().order_by('size')

    # Filter carries based on position and size
    filtered_carries = Carry.objects.filter(position__in=positions, size__in=sizes)

    # Annotate with the total count of names
    annotated_carries = filtered_carries.values('position', 'size').annotate(total_count=Count('name'))

    # Create a dictionary to quickly access the total counts of carries
    total_carries = {}
    for carry in annotated_carries:
        position = carry['position']
        size = carry['size']
        count = carry['total_count']

        if position not in total_carries:
            total_carries[position] = {}
        total_carries[position][size] = count

    # Get done carries by the user in one query
    user_done_carries = DoneCarry.objects.filter(user=user).select_related('carry')

    # Get todo carries by the user in one query, prefetching the related Carry objects
    user_todo_carries = TodoCarry.objects.filter(user=user).prefetch_related('carry')

    # Get the carry names from the related Carry objects
    user_todo_names = [todo_carry.carry.name for todo_carry in user_todo_carries]

    # Get all carries with an annotation for whether they are in the user's todo list
    all_carries_ann = (
        Carry.objects.annotate(
            intodo=Case(
                When(name__in=user_todo_names, then=True),
                default=False,
                output_field=BooleanField(),
            )
        )
        .values('name', 'longtitle', 'position', 'intodo')
        .order_by('longtitle')  # Sort directly at the database level
    )

    # Get image urls
    todo_data = []
    for carry in user_todo_carries:
        url = utils.generate_carry_url(carry.carry.name, carry.carry.position)

        # Append the carry title and image URL to the list
        todo_data.append({
            'title': carry.carry.title,
            'name': carry.carry.name,
            'image_url': url
        })
    
    # Create structures for user carries
    done_counts = {}
    done_carry_names = {}
    
    # Initialize the structures for positions
    for position in positions:
        done_counts[position] = {}
        done_carry_names[position] = {}
        
        for size in sizes:
            # Filter user done carries by position and size
            user_done = user_done_carries.filter(
                carry__position=position,
                carry__size=size
            )
            
            # Done count and names of done carries
            done_counts[position][size] = user_done.count()
            done_carry_names[position][size] = list(
                user_done.values_list('carry__name', flat=True))

    # Pass the separated carries information to the template
    context = {
        'all_carries_ann': all_carries_ann,
        'positions': positions,
        'sizes': sizes,
        'total_carries': total_carries,
        'done_counts': done_counts,
        'done_carry_names': done_carry_names,
        'todo_carries': todo_data,
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
        is_todo = TodoCarry.objects.filter(carry=carry, user=user).exists()
        
        # Fetch the user's rating for the carry, if it exists
        user_rating = UserRating.objects.filter(carry=carry, user=user).first()

        if user_rating:
            user_ratings_data = user_rating.to_dict()
    else:
        is_done = False
        is_todo = False

    # Get the carry context
    carry_context = utils.get_carry_context(name)
    
    # Add 'is_done' and user ratings to the context
    context = {
        **carry_context,
        'is_done': is_done,
        'is_todo': is_todo,
        'user_ratings': user_ratings_data,
    }

    return render(request, "wrappinggallery/carry.html", context)

@require_POST
def file_url(request):
     # Parse the request body as JSON to get the data sent in the POST request
    body = json.loads(request.body)
    file_name = body.get("file_name")
    position = body.get("position", "back")

    image_url = utils.generate_carry_url(file_name, position)

    return JsonResponse({"url": image_url})


def achievement_file_url(request, file_name):
    image_url = utils.generate_achievement_url(file_name)

    return JsonResponse({"url": image_url})


@require_GET
def carry_count(request):
    count = Carry.objects.count()
    return JsonResponse({'count': count})


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
@require_POST
def mark_as_done(request, carry_name):
    carry = get_object_or_404(Carry, name=carry_name)
    user = request.user

    achieved_before = UserAchievement.objects.filter(
        Q(user=user) & (Q(achievement__category=1) | Q(achievement__category=0))
    )
    achieved_before = set(achieved_before.values_list(
        'achievement__title', 'achievement__name', 'achievement__description',
    ))
    
    # Check if the done already entry exists
    if not DoneCarry.objects.filter(carry=carry, user=user).exists():
        DoneCarry.objects.create(carry=carry, user=user)

    achieved_after = UserAchievement.objects.filter(
        Q(user=user) & (Q(achievement__category=1) | Q(achievement__category=0))
    )        
    
    achieved_after = set(achieved_after.values_list(
        'achievement__title', 'achievement__name', 'achievement__description',
    ))

    unlocked = [{'name': tuple_[1], 'title': tuple_[0], 'description':  tuple_[2]} for tuple_ in list(achieved_after - achieved_before)]
    
    # Return a JSON response
    return JsonResponse({'unlocked_achievements': unlocked})


@login_required
@require_POST
def add_to_todo(request, carry_name):
    carry = get_object_or_404(Carry, name=carry_name)
    user = request.user
    
    # Check if the done already entry exists
    if not TodoCarry.objects.filter(carry=carry, user=user).exists():
        TodoCarry.objects.create(carry=carry, user=user)

    
    # Return a JSON response
    return JsonResponse({})


@login_required
@require_POST
def remove_done(request, carry_name):
    carry = get_object_or_404(Carry, name=carry_name)
    user = request.user

    # Remove from favorites if it exists
    done_carries = DoneCarry.objects.filter(carry=carry, user=user)
    for done_carry in done_carries:
        done_carry.delete()

    return JsonResponse({})


@login_required
@require_POST
def remove_todo(request, carry_name):
    carry = get_object_or_404(Carry, name=carry_name)
    user = request.user

    # Remove from favorites if it exists
    todo_carries = TodoCarry.objects.filter(carry=carry, user=user)
    for todo_carry in todo_carries:
        todo_carry.delete()

    return JsonResponse({})


@login_required
def get_done_carries(request):
    if request.user.is_authenticated:
        carries = DoneCarry.objects.filter(user=request.user).values_list('carry__name', flat=True)
        return JsonResponse({"carries": list(carries)})
    else:
        return JsonResponse({"error": "User not authenticated"}, status=403)


@login_required
@require_POST
def submit_review(request, carry_name):
    # Get the rating values from the form
    user = request.user

    # Get list of review-related achievements from this user
    achieved_before = UserAchievement.objects.filter(
        Q(user=user) & (Q(achievement__category=2) | Q(achievement__category=0))
    )
    achieved_before = set(achieved_before.values_list(
        'achievement__title', 'achievement__name', 'achievement__description',
    ))

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

    achieved_after = UserAchievement.objects.filter(
        Q(user=user) & (Q(achievement__category=2) | Q(achievement__category=0))
    )
    
    achieved_after = set(achieved_after.values_list(
        'achievement__title', 'achievement__name', 'achievement__description',
    ))
    unlocked = [{'name': tuple_[1], 'title': tuple_[0], 'description':  tuple_[2]} for tuple_ in list(achieved_after - achieved_before)]
    
    return JsonResponse({'unlocked_achievements': unlocked})
