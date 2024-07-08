from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/filter-carries/", views.filter_carries, name="filter_carries"),
]
