from supabase import create_client, Client
from django.conf import settings
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.http import JsonResponse
import os


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

     except Exception as e:
        return None

def generate_signed_url_wrapper(file_path, bucket, supabase=supabase_client):
    result = generate_signed_url(file_path, bucket, supabase)

    if result is None:
        return None

    return (file_path, result)


def generate_signed_urls(file_paths, bucket, supabase=supabase_client):
    signed_urls = {}

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_signed_url_wrapper, file_path, bucket, supabase) for file_path in file_paths]
        for future in as_completed(futures):
            if future.result() is not None:
                signed_urls[future.result()[0]] = future.result()[1]

    return signed_urls


def generate_server_url(file_name, position):
    static_url = settings.STATIC_URL + "/wrappinggallery/illustrations/"
    static_path = os.path.join(settings.STATIC_ROOT, "wrappinggallery", "illustrations")

    image_url = static_url + f"{file_name}.png"
    image_path = os.path.join(static_path, f"{file_name}.png")
    
    if not os.path.exists(image_path):
        if position in ["back", "front"]:
            image_url = static_url + f"placeholder_{position}.png"
            image_path = os.path.join(static_path, f"placeholder_{position}.png")
        else:
            print("error position not valid", file_name, position)
            exit(1)

        assert os.path.exists(image_path)


    return image_url
