from supabase import create_client
from django.conf import settings

def generate_signed_url(file_path):
    supabase = create_client(settings.SUPABASE_URL, settings.SERVICE_ROLE_KEY)
    
    try:
        response = supabase.storage.from_(settings.SUPABASE_BUCKET_NAME).create_signed_url(file_path, expires_in=3600)
        return response['signedURL']

    except Exception as e:
        print(f"Error generating signed URL: {e}")
        return None


