from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import (
    Achievement,
    Carry,
    CustomUser,
    DoneCarry,
    FavouriteCarry,
    Rating,
    TodoCarry,
    UserAchievement,
    UserRating,
)

# Register your models here.
admin.site.register(Carry)
admin.site.register(Rating)
admin.site.register(FavouriteCarry)
admin.site.register(DoneCarry)
admin.site.register(TodoCarry)
admin.site.register(UserRating)
admin.site.register(UserAchievement)
admin.site.register(Achievement)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
