from supabase import create_client, Client
from django.conf import settings


def initialise_supabase():
    url: str = settings.SUPABASE_URL
    key: str = settings.SERVICE_ROLE_KEY
    return create_client(url, key)


def generate_signed_url(file_path, bucket):
    supabase: Client = initialise_supabase()

    try:
        response = supabase.storage.from_(bucket).create_signed_url(
            file_path, expires_in=3600
        )

        return response["signedURL"]

    except Exception as e:
        print(f"Error generating signed URL: {e}")
        return None
