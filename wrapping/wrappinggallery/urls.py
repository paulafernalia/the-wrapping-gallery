from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("termsandconditions/", views.termsandconditions, name="termsandconditions"),
    path("faq/", views.faq, name="faq"),
    path("api/filter-carries/", views.filter_carries, name="filter_carries"),
    path("carry/<str:name>", views.carry, name="carry"),
    path("file-url/<str:file_name>/", views.file_url, name="file_url"),
    path("step-urls/<str:prefix>/", views.steps_url, name="file_url"),
    path('downloads/', views.downloads, name='downloads'),
    path('download-booklet/<str:carry>', views.download_booklet, name='download_booklet'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
]
