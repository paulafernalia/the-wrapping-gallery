from django.urls import path
from . import views
from .sitemaps import StaticViewSitemap, CarrySitemap
from django.contrib.sitemaps.views import sitemap


sitemaps = {
    'static': StaticViewSitemap,
    'carry': CarrySitemap,
}


urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("termsandconditions/", views.termsandconditions, name="termsandconditions"),
    path("faq/", views.faq, name="faq"),
    path("api/filter-carries/", views.filter_carries, name="filter_carries"),
    path("carry/<str:name>", views.carry, name="carry"),
    path("file-url/", views.file_url, name="file_url"),
    path("achievement-file-url/<str:file_name>/", views.achievement_file_url, name="achievement_file_url"),
    path("step-urls/<str:prefix>/", views.steps_url, name="file_url"),
    path('downloads/', views.downloads, name='downloads'),
    path('download-booklet/<str:carry>', views.download_booklet, name='download_booklet'),
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),  # If using class-based view
    path('collection/', views.collection, name="collection"),
    path('mark-done/<str:carry_name>/', views.mark_as_done, name='mark_as_done'),
    path('add-todo/<str:carry_name>/', views.add_to_todo, name='add_to_todo'),
    path('remove-done/<str:carry_name>/', views.remove_done, name='remove_done'),
    path('remove-todo/<str:carry_name>/', views.remove_todo, name='remove_todo'),
    path('done-carries/', views.get_done_carries, name='get_done_carries'),
    path('submit-review/<str:carry_name>/', views.submit_review, name='submit_review'),
    path('achievements/', views.achievements, name="achievements"),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/delete_account/', views.delete_account, name='delete_account'),
    path('accounts/account-deleted/', views.account_deleted, name='account_deleted'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]
