from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Carry

# Sitemap for static pages
class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['faq', 'index', 'about', 'downloads']

    def location(self, item):
        return reverse(item)

# Sitemap for the Carry model
class CarrySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Carry.objects.all()

    def location(self, obj):
        return reverse('carry', args=[obj.name])