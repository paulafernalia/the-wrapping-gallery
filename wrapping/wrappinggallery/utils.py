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
            queryset = queryset.filter(
                Q(carry__title__icontains=val)
                | Q(carry__longtitle__icontains=val)
                | Q(carry__name__icontains=val)
                | Q(carry__finish__icontains=val)
            )
        elif prop == "pretied" and val == "1":
            queryset = queryset.filter(carry__pretied=val)
        elif prop == "tutorial" and val == "1":
            queryset = queryset.filter(carry__tutorial=val)
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
        elif prop == "pregnancy" and val == "1":
            queryset = queryset.filter(pregnancy__gte=3.5)
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

    return queryset
