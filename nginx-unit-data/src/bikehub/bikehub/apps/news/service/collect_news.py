import pathlib

import feedparser
import pandas as pd
from common_modules.service.image.get_image import get_remote_image
from django.core.files import File
from django.core.mail import send_mail
from django.db.models import Q
from news.models import (ContentTag, News, SourseSite, SubCategoryTagMap,
                         TargetSite)

from .find_content import FindContents
from .find_img import FindImg
from .find_tag import FindTag

DISALLOW_WORDS = ('自転車', 'マウンテンバイク', 'ロードバイク',)


class CollectNews():
    def collect_news(self):
        target_sites = TargetSite.objects.filter(deactive=False).all()
        # with ThreadPoolExecutor() as w:
        #     w.map(self.collect, target_sites)
        for target_site in target_sites:
            self.collect(target_site)

    def collect(self, target):
        fi = FindImg()
        fc = FindContents()
        target_url = target.rss_url

        summary = ''
        is_active = False
        try:
            feeds = feedparser.parse(target_url)
        except Exception as e:
            print(e)
            print("34 : collect_news")
            return
        is_skip = False

        entries = feeds['entries']

        # print(feeds['entries'])
        if(len(entries)):
            # get each contents
            for entriy in entries:
                tmp_summary = ''
                tag_maps = []
                source_site = None

                page_url = entriy['links'][0]['href']
                title = entriy['title']

                featured_image = None
                content_text = None
                featured_image = fi.find_img(
                    entriy, feeds, page_url, target_url
                )

                if target.is_there_another_source:
                    tags = ContentTag.objects.all()

                    source_site, created = SourseSite.objects.get_or_create(
                        name=entriy['source']['title'],
                        sorce_url=entriy['source']['href']
                    )

                    del created

                    def _get_contents(tags: list) -> str:
                        for tag in tags:
                            content_text = fc.find_contents(
                                page_url,
                                tag.tag_type,
                                tag.tag_class_name,
                                tag.tag_id_name
                            )

                            if content_text:
                                return content_text

                    content_text = _get_contents(tags)

                else:
                    content_text = fc.find_contents(
                        page_url,
                        target.content_tag.tag_type,
                        target.content_tag.tag_class_name,
                        target.content_tag.tag_id_name
                    )

                if not content_text:
                    is_skip = True
                    content_text = ''

                # create summary
                tmp_summary = [
                    a for a in content_text.split() if a != '' and not len(a) < 20
                ]

                check_title = title.replace('【トピックス】', '')

                summary = '\n'.join(tmp_summary)
                summary = summary[:1000]
                # only save the content that has img and content_text
                for key in DISALLOW_WORDS:
                    if key in title:
                        is_skip = True

                if content_text != '' and not is_skip:
                    exists = News.objects.filter(
                        Q(
                            title=check_title
                        )
                    ).exists()

                    if not exists:
                        topThree = News.objects.order_by(
                            '-created_at'
                        ).all()[:2]

                        IsContinuous = True
                        for n in topThree:
                            if n.site.pk != target.pk:
                                IsContinuous = False

                        if not IsContinuous or target.is_there_another_source:
                            featured_image = featured_image if featured_image is not None else ''
                            if featured_image in ('', None):
                                is_skip = True

                            if not is_skip:

                                try:
                                    # create news contens
                                    news_obj, created = News.objects.get_or_create(
                                        url=page_url,
                                    )

                                    if created and news_obj.featured_image and not news_obj.owned_featured_image:
                                        tmp_img = get_remote_image(news_obj.featured_image)
                                        if tmp_img:
                                            news_obj.title = title
                                            news_obj.summary = summary
                                            news_obj.target = target
                                            news_obj.featured_image = featured_image
                                            news_obj.source_site = source_site

                                            extension = pathlib.Path(
                                                news_obj.featured_image).suffix
                                            news_obj.owned_featured_image.save(
                                                f"image_{news_obj.pk}{extension}", File(tmp_img)
                                            )
                                            img = news_obj.owned_featured_image
                                            news_obj.featured_image = f'https://dlnqgsc0jr0k.cloudfront.net/{img}'
                                            news_obj.save()
                                            # find tag and grouping same tags
                                            data = pd.DataFrame({
                                                'tags': FindTag.find_tag(content_text)
                                            }).groupby(
                                                ['tags']
                                            ).size().reset_index(
                                                name='counts'
                                            )
                                            # create tag
                                            result = FindTag.create_tag(data)
                                            for r in result:
                                                if r.related_of_maker_id or r.main_category_tag_id:
                                                    tag_maps.append(SubCategoryTagMap(
                                                        sub_category_tag=r,
                                                        news=news_obj
                                                    ))

                                            SubCategoryTagMap.objects.bulk_create(
                                                tag_maps)
                                            target.reason = ''
                                        else:
                                            news_obj.delete()

                                except Exception as e:
                                    print(e)
                                    # send_mail(
                                    #     '【batch news result】',
                                    #     f'you got error \n {e}',
                                    #     'batch@bikehub.app',
                                    #     ['yuta322@gmail.com'],
                                    #     fail_silently=False,
                                    # )
            is_active = True

        else:
            target.reason = 'can not find feeds["entries"]'

        target.is_active = is_active
        target.save()

    # def create_news(self):
    #     all_target = TargetSite.objects.all().filter(name="").filter(url="").values()
    #     for target in all_target:
    #         parsed_url = urlparse(target['rss_url'])
    #         print(parsed_url)

    # def create_tags(self, news_title):
    #     print('')
