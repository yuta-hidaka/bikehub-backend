from django.db import models

# Create your models here.


class TargetSite(models.Model):
    name = models.CharField(max_length=150, blank=True, default='')
    rss_url = models.URLField()
    url = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'news_target_site'


class Tag(models.Model):
    name = models.CharField(max_length=150, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'news_tag'


class News(models.Model):
    title = models.CharField(max_length=150, blank=True, default='')
    url = models.URLField()
    site = models.ForeignKey(TargetSite, on_delete=models.CASCADE)
    published_at = models.DateTimeField()
    featured_image = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'news'


class TagMap(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (str(self.tag) + ' : ' + str(self.news))

    class Meta:
        db_table = 'news_tag_map'
