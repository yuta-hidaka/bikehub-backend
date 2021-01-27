# myproject/sitemaps.py

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from news.models import News


class NewsSitemap(Sitemap):
    """
    News
    """
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return News.objects.filter(show=True).all()

    # モデルに get_absolute_url() が定義されている場合は不要
    # def location(self, obj):
    #     return reverse('news:post_detail', args=[obj.pk])

    def lastmod(self, obj):
        return obj.updated_at


class StaticViewSitemap(Sitemap):
    """
    静的ページのサイトマップ
    """
    changefreq = "daily"
    priority = 0.5

    # def items(self):
    #     return ['news:index', 'news:fc']

    # def location(self, item):
    #     return reverse(item)
