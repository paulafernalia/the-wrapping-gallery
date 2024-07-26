from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("api/filter-carries/", views.filter_carries, name="filter_carries"),
    path("carry/<str:name>", views.carry, name="carry"),
    path("file-url/<str:file_name>/", views.file_url, name="file_url"),
]
