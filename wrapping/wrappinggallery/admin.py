from django.contrib import admin
from .models import Carry, Ratings, UserRatings

# Register your models here.
admin.site.register(Carry)
admin.site.register(Ratings)
admin.site.register(UserRatings)
