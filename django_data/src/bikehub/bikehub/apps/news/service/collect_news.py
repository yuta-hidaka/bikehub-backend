from news.models import *
from django.db import models
import feedparser
import json
from urllib.parse import urlparse
import lxml.html
from urllib.request import urlopen
from urllib.parse import urljoin
import datetime
# Create your models here.


# class TargetSite(models.Model):
#     name = models.CharField(max_length=150, blank=True, default='')
#     rss_url = models.URLField()
#     url = models.URLField(blank=True, default='')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = 'news_target_site'


# class Tag(models.Model):
#     name = models.CharField(max_length=150, blank=True, default='')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = 'news_tag'


# class News(models.Model):
#     title = models.CharField(max_length=150, blank=True, default='')
#     url = models.URLField()
#     site = models.ForeignKey(TargetSite, on_delete=models.CASCADE)
#     published_at = models.DateTimeField()
#     featured_image = models.URLField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title

#     class Meta:
#         db_table = 'news'


# class TagMap(models.Model):
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
#     news = models.ForeignKey(News, on_delete=models.CASCADE)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return (str(self.tag) + ' : ' + str(self.news))

#     class Meta:
#         db_table = 'news_tag_map'


class CollectNews():
    def findImg(self, link):
        tree = lxml.html.parse(urlopen(link))
        html = tree.getroot()
        # 画像URLの取得
        try:
            # urljoinで相対パス→絶対パス
            img = urljoin(link, html.cssselect(
                'img.photo_table__img')[0].attrib['src'])
        # 画像がない場合はFalseが入る
        except(IndexError):
            return False
        return img

    def createNewsDetail(self):
        all_target = TargetSite.objects.all()

        for target in all_target:
            feeds = feedparser.parse(target.rss_url)
            for entrie in feeds['entries']:
                # print(json.dumps(entrie, indent=4, ensure_ascii=False))
                try:
                    # print(entrie['summary'])
                    pass
                except :
                    pass
                # print(entrie['summary'])
                # print(entrie['title'])
                # print(entrie['links'][0]['href'])
                a=self.findImg(entrie['links'][0]['href'])
                print(a)

    def createNewsSiteDetail(self):
        all_target = TargetSite.objects.all().filter(name="").filter(url="").values()
        for target in all_target:
            parsed_url = urlparse(target['rss_url'])
            print(parsed_url)

    def findNewsTag(self, news_title):
        print('')
