from django.contrib import admin
from .models import Carry, Rating, FavouriteCarry, DoneCarry, TodoCarry

from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

# Register your models here.
admin.site.register(Carry)
admin.site.register(Rating)
admin.site.register(FavouriteCarry)
admin.site.register(DoneCarry)
admin.site.register(TodoCarry)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username",]

admin.site.register(CustomUser, CustomUserAdmin)

