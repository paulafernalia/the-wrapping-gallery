from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Carry

# Sitemap for static pages
class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['faq', 'index', 'about', 'downloads']

    def location(self, item):
        return reverse(item)


# Sitemap for the Carry model
class CarrySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return Carry.objects.order_by('name')

    def location(self, obj):
        return reverse('carry', args=[obj.name])

    def lastmod(self, item):
        return item.updated_at