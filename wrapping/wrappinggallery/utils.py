from concurrent.futures import ThreadPoolExecutor, as_completed

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db.models import Q
from supabase import create_client

from .models import Carry, Rating


def initialise_supabase():
    url: str = settings.SUPABASE_URL
    key: str = settings.SERVICE_ROLE_KEY
    return create_client(url, key)


supabase_client = initialise_supabase()


def generate_signed_url(file_path, bucket, supabase=supabase_client):
    try:
        response = supabase.storage.from_(bucket).create_signed_url(
            file_path, expires_in=3600
        )

        return response["signedURL"]

    except Exception:
        return None


def generate_signed_url_wrapper(file_path, bucket, supabase=supabase_client):
    result = generate_signed_url(file_path, bucket, supabase)

    if result is None:
        return None

    return (file_path, result)


def generate_signed_urls(file_paths, bucket, supabase=supabase_client):
    signed_urls = {}

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(generate_signed_url_wrapper, file_path, bucket, supabase)
            for file_path in file_paths
        ]
        for future in as_completed(futures):
            if future.result() is not None:
                signed_urls[future.result()[0]] = future.result()[1]

    return signed_urls


def generate_profile_url():
    filepath = "wrappinggallery/illustrations/profile.png"
    assert staticfiles_storage.exists(filepath)

    image_url = staticfiles_storage.url(filepath)

    return image_url


def generate_carry_url(carry, position, dark=False):
    if not dark:
        filepath = f"wrappinggallery/illustrations/carries/{carry}.png"
    else:
        filepath = f"wrappinggallery/illustrations/carries/{carry}_dark.png"

    if not staticfiles_storage.exists(filepath):
        if position in ["back", "front", "tandem"]:
            if dark:
                filepath = f"wrappinggallery/illustrations/carries/placeholder_{position}_dark.png"
            else:
                filepath = (
                    f"wrappinggallery/illustrations/carries/placeholder_{position}.png"
                )
            assert staticfiles_storage.exists(filepath)
        else:
            print("error position not valid", carry, position)
            exit(1)

    image_url = staticfiles_storage.url(filepath)

    return image_url


def generate_achievement_url(achievement):
    filepath = f"wrappinggallery/illustrations/achievements/{achievement}.png"

    if not staticfiles_storage.exists(filepath):
        filepath = "wrappinggallery/illustrations/carries/placeholder_front.png"
        filepath = "wrappinggallery/illustrations/carries/placeholder_front.png"
        assert staticfiles_storage.exists(filepath)

    image_url = staticfiles_storage.url(filepath)

    return image_url


def get_carry_context(name):
    queryset = Carry.objects.all().filter(name=name)
    assert len(queryset) == 1

    carry_dict = queryset[0].to_dict()

    if carry_dict["videoauthor"] == "" or carry_dict["videoauthor"] is None:
        assert carry_dict["videotutorial"] == "" or carry_dict["videotutorial"] is None
        carry_dict["videoauthor"] = "NA"
        carry_dict["videotutorial"] = "NA"

    if carry_dict["videoauthor2"] == "" or carry_dict["videoauthor2"] is None:
        assert (
            carry_dict["videotutorial2"] == "" or carry_dict["videotutorial2"] is None
        )
        carry_dict["videoauthor2"] = "NA"
        carry_dict["videotutorial2"] = "NA"

    if carry_dict["videoauthor3"] == "" or carry_dict["videoauthor3"] is None:
        assert (
            carry_dict["videotutorial3"] == "" or carry_dict["videotutorial3"] is None
        )
        carry_dict["videoauthor3"] = "NA"
        carry_dict["videotutorial3"] = "NA"

    image_url = generate_carry_url(name, carry_dict["position"].lower(), True)
    carry_dict["imageSrc"] = image_url

    ratingsqueryset = Rating.objects.all().filter(carry__name=name)
    assert len(ratingsqueryset) == 1

    carry_context = {**carry_dict, **(ratingsqueryset[0].to_dict())}
    return carry_context


def apply_filters(queryset, properties, values, mmpositions, finishes, difficulties):
    """Apply filters to queryset based on properties and values."""

    # Combined filter mapping for better organization
    FILTER_HANDLERS = {
        # Simple filters
        "position": lambda val: Q(carry__position=val.lower())
        if val not in ["Any", "null"]
        else None,
        "shoulders": lambda val: Q(carry__shoulders=val)
        if val not in ["Any", "null"]
        else None,
        "pretied": lambda val: Q(carry__pretied=val) if val == "1" else None,
        "tutorial": lambda val: Q(carry__tutorial=val) if val == "1" else None,
        "rings": lambda val: Q(carry__rings=val) if val == "1" else None,
        # Special cases with closures
        "layers": lambda val: _handle_layers_filter(val),
        "mmposition": lambda val: _handle_mmposition_filter(val, mmpositions),
        "finish": lambda val: _handle_finish_filter(val, finishes),
        "partialname": lambda val: _handle_partialname_filter(val),
    }

    # Generate pass and other filters dynamically
    pass_fields = [
        "sling",
        "ruck",
        "kangaroo",
        "cross",
        "reinforcing_cross",
        "reinforcing_horizontal",
        "horizontal",
        "poppins",
    ]
    other_fields = [
        "chestpass",
        "bunchedpasses",
        "shoulderflip",
        "twistedpass",
        "waistband",
        "legpasses",
        "s2s",
        "eyelet",
        "poppins",
        "sternum",
    ]
    rating_fields = [
        "newborns",
        "pregnancy",
        "legstraighteners",
        "leaners",
        "bigkids",
        "feeding",
        "quickups",
        "fancy",
    ]

    # Add dynamically generated filters
    _add_generated_filters(FILTER_HANDLERS, pass_fields, other_fields, rating_fields)

    # Apply filters
    for prop, val in zip(properties, values, strict=False):
        if prop in FILTER_HANDLERS:
            filter_q = FILTER_HANDLERS[prop](val)
            if filter_q:
                queryset = queryset.filter(filter_q)

    return queryset


def _add_generated_filters(handlers, pass_fields, other_fields, rating_fields):
    """Add dynamically generated filter handlers to reduce repetition."""

    # Add pass filters (positive and negative)
    for field in pass_fields:
        handlers[f"pass_{field}"] = (
            lambda val, f=field: Q(**{f"carry__pass_{f}": val}) if val == "1" else None
        )
        handlers[f"no_pass_{field}"] = (
            lambda val, f=field: Q(**{f"carry__pass_{f}": "0"}) if val == "1" else None
        )

    # Add other filters (positive and negative)
    for field in other_fields:
        handlers[f"other_{field}"] = (
            lambda val, f=field: Q(**{f"carry__other_{f}": val}) if val == "1" else None
        )
        handlers[f"no_other_{field}"] = (
            lambda val, f=field: Q(**{f"carry__other_{f}": "0"}) if val == "1" else None
        )

    # Add rating filters
    for field in rating_fields:
        handlers[field] = (
            lambda val, f=field: Q(**{f"{f}__gte": 3.5}) if val == "1" else None
        )


def _handle_layers_filter(val):
    """Handle layers filter logic."""
    if val in ["Any", "null"]:
        return None
    return Q(carry__layers=-1) if val == "Varies" else Q(carry__layers=val)


def _handle_mmposition_filter(val, mmpositions):
    """Handle mmposition filter logic."""
    return Q(carry__mmposition=mmpositions[val]) if val not in ["Any", "null"] else None


def _handle_finish_filter(val, finishes):
    """Handle finish filter logic."""
    return Q(carry__finish=finishes[val]) if val not in ["Any", "null"] else None


def _handle_partialname_filter(val):
    """Handle partial name search filter logic."""
    if val in ["null", ""] or not val:
        return None

    return (
        Q(carry__title__icontains=val)
        | Q(carry__longtitle__icontains=val)
        | Q(carry__name__icontains=val)
        | Q(carry__finish__icontains=val)
    )
