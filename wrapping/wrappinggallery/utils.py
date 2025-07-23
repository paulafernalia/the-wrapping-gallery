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

    # Define filter mappings for simple field filters
    SIMPLE_FILTERS = {
        "position": lambda val: Q(carry__position=val.lower())
        if val not in ["Any", "null"]
        else None,
        "shoulders": lambda val: Q(carry__shoulders=val)
        if val not in ["Any", "null"]
        else None,
        "pretied": lambda val: Q(carry__pretied=val) if val == "1" else None,
        "tutorial": lambda val: Q(carry__tutorial=val) if val == "1" else None,
        "rings": lambda val: Q(carry__rings=val) if val == "1" else None,
    }

    # Define pass filters (positive)
    PASS_FILTERS = {
        "pass_sling": "carry__pass_sling",
        "pass_ruck": "carry__pass_ruck",
        "pass_kangaroo": "carry__pass_kangaroo",
        "pass_cross": "carry__pass_cross",
        "pass_reinforcing_cross": "carry__pass_reinforcing_cross",
        "pass_reinforcing_horizontal": "carry__pass_reinforcing_horizontal",
        "pass_horizontal": "carry__pass_horizontal",
        "pass_poppins": "carry__pass_poppins",
    }

    # Define negative pass filters
    NO_PASS_FILTERS = {
        "no_pass_sling": "carry__pass_sling",
        "no_pass_ruck": "carry__pass_ruck",
        "no_pass_kangaroo": "carry__pass_kangaroo",
        "no_pass_cross": "carry__pass_cross",
        "no_pass_reinforcing_cross": "carry__pass_reinforcing_cross",
        "no_pass_reinforcing_horizontal": "carry__pass_reinforcing_horizontal",
        "no_pass_horizontal": "carry__pass_horizontal",
        "no_pass_poppins": "carry__pass_poppins",
    }

    # Define other filters (positive)
    OTHER_FILTERS = {
        "other_chestpass": "carry__other_chestpass",
        "other_bunchedpasses": "carry__other_bunchedpasses",
        "other_shoulderflip": "carry__other_shoulderflip",
        "other_twistedpass": "carry__other_twistedpass",
        "other_waistband": "carry__other_waistband",
        "other_legpasses": "carry__other_legpasses",
        "other_s2s": "carry__other_s2s",
        "other_eyelet": "carry__other_eyelet",
        "other_poppins": "carry__other_poppins",
        "other_sternum": "carry__other_sternum",
    }

    # Define negative other filters
    NO_OTHER_FILTERS = {
        "no_other_chestpass": "carry__other_chestpass",
        "no_other_bunchedpasses": "carry__other_bunchedpasses",
        "no_other_shoulderflip": "carry__other_shoulderflip",
        "no_other_twistedpass": "carry__other_twistedpass",
        "no_other_waistband": "carry__other_waistband",
        "no_other_legpasses": "carry__other_legpasses",
        "no_other_s2s": "carry__other_s2s",
        "no_other_eyelet": "carry__other_eyelet",
        "no_other_sternum": "carry__other_sternum",
        "no_other_poppins": "carry__other_poppins",
    }

    # Define rating filters (>= 3.5)
    RATING_FILTERS = {
        "newborns",
        "pregnancy",
        "legstraighteners",
        "leaners",
        "bigkids",
        "feeding",
        "quickups",
        "fancy",
    }

    for prop, val in zip(properties, values, strict=False):
        filter_q = None

        # Handle simple filters
        if prop in SIMPLE_FILTERS:
            filter_q = SIMPLE_FILTERS[prop](val)

        # Handle special cases
        elif prop == "layers":
            filter_q = _handle_layers_filter(val)
        elif prop == "mmposition":
            filter_q = _handle_mmposition_filter(val, mmpositions)
        elif prop == "finish":
            filter_q = _handle_finish_filter(val, finishes)
        elif prop == "partialname":
            filter_q = _handle_partialname_filter(val)

        # Handle pass filters
        elif prop in PASS_FILTERS and val == "1":
            filter_q = Q(**{PASS_FILTERS[prop]: val})
        elif prop in NO_PASS_FILTERS and val == "1":
            filter_q = Q(**{NO_PASS_FILTERS[prop]: "0"})

        # Handle other filters
        elif prop in OTHER_FILTERS and val == "1":
            filter_q = Q(**{OTHER_FILTERS[prop]: val})
        elif prop in NO_OTHER_FILTERS and val == "1":
            filter_q = Q(**{NO_OTHER_FILTERS[prop]: "0"})

        # Handle rating filters
        elif prop in RATING_FILTERS and val == "1":
            filter_q = Q(**{f"{prop}__gte": 3.5})

        # Apply the filter if one was created
        if filter_q:
            queryset = queryset.filter(filter_q)
    return queryset


def _handle_layers_filter(val):
    """Handle layers filter logic."""
    if val in ["Any", "null"]:
        return None
    elif val == "Varies":
        return Q(carry__layers=-1)
    else:
        return Q(carry__layers=val)


def _handle_mmposition_filter(val, mmpositions):
    """Handle mmposition filter logic."""
    if val not in ["Any", "null"]:
        return Q(carry__mmposition=mmpositions[val])
    return None


def _handle_finish_filter(val, finishes):
    """Handle finish filter logic."""
    if val not in ["Any", "null"]:
        return Q(carry__finish=finishes[val])
    return None


def _handle_partialname_filter(val):
    """Handle partial name search filter logic."""
    if val not in ["null", ""] and val:
        return (
            Q(carry__title__icontains=val)
            | Q(carry__longtitle__icontains=val)
            | Q(carry__name__icontains=val)
            | Q(carry__finish__icontains=val)
        )
    return None
