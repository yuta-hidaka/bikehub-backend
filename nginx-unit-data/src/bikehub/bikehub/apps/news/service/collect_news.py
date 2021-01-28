import pathlib

import feedparser
import pandas as pd
from _youtube.service.search_on_youtube import youtube
from common_modules.service.image.image import get_remote_image
from django.core.files import File
# from django.core.mail import send_mail
from django.db.models import Q
from news.models import News, SourseSite, SubCategoryTagMap, TargetSite

from .find_content import FindContents
from .find_img import FindImg
from .find_tag import FindTag
from .summary import Summary

DISALLOW_WORDS = ('自転車', 'マウンテンバイク', 'ロードバイク',)


class CollectNews():
    def collect_news(self):
        target_sites = TargetSite.objects.filter(deactive=False).all()
        # with ThreadPoolExecutor() as w:
        #     w.map(self.collect, target_sites)
        for target_site in target_sites:
            self.collect(target_site)

    def collect(self, target):
        target_url = target.rss_url
        entries = []
        if target.is_youtube:
            feeds = None
            entries = youtube().search(query=target.youtube_query)
        else:
            try:
                feeds = feedparser.parse(target_url)
            except Exception as e:
                print(e)
                print("34 : collect_news")
                return
            entries = feeds['entries']

        def __create(target_url: str, entries: dict):
            fi = FindImg()
            fc = FindContents()
            summary = Summary()
            if(not len(entries)):
                target.reason = 'can not find feeds["entries"]'
                return

            # get each contents
            for entriy in entries:
                is_skip = False
                source_site = None
                page_url = entriy['links'][0]['href']
                title = entriy['title']
                summary_str = ''
                content_text = None
                featured_image = None
                
                if target.is_youtube:
                    summary_str = entriy.get('summary', '')
                    content_text = entriy.get('summary')
                    featured_image = entriy.get('featured_image')

                if not featured_image:
                    featured_image = fi.find_img(
                        entriy=entriy, feeds=feeds, page_url=page_url
                    )

                if (target.is_there_another_source or target.is_youtube) and featured_image:
                    if featured_image.startswith('//'):
                        featured_image = 'https:' + featured_image
                    source_site, created = SourseSite.objects.get_or_create(
                        name=entriy['source']['title'],
                        sorce_url=entriy['source']['href']
                    )
                    del created
                    if not content_text:
                        content_text = fc.find_contents_by_tags(target_url)

                elif target.content_tag:
                    if not content_text:
                        content_text = fc.find_contents(
                            page_url,
                            target.content_tag.tag_type,
                            target.content_tag.tag_class_name,
                            target.content_tag.tag_id_name
                        )

                if not content_text:
                    content_text = title
                else:
                    if not summary_str or not target.is_youtube:
                        summary_str = summary.create(content_text)

                is_skip = self.news_check(
                    title, content_text, page_url, target, source_site, featured_image
                )
                if is_skip:
                    return

                created = False
                try:
                    # create news contens
                    news_obj, created = News.objects.get_or_create(
                        title=title,
                        summary=summary_str,
                        url=page_url,
                        site=target,
                        featured_image=featured_image,
                        source_site=source_site,
                        is_youtube=target.is_youtube,
                        video_id=entriy.get('video_id', ''),
                        show=(not target.hide_post  )
                    )
                except Exception as e:
                    print(
                        f'This happend from collect news create on get_or_create \n {e}')

                if not created:
                    return

                tmp_img = get_remote_image(news_obj.featured_image)
                if not tmp_img and not news_obj.featured_image and news_obj.owned_featured_image:
                    news_obj.delete()

                extension = pathlib.Path(
                    news_obj.featured_image).suffix
                news_obj.owned_featured_image.save(
                    f"featured_image_{news_obj.pk}{extension}",
                    File(tmp_img)
                )
                news_obj.thumbnail_image.save(
                    f"thumbnail_image_{news_obj.pk}{extension}",
                    File(tmp_img)
                )
                # img = news_obj.owned_featured_image
                # news_obj.featured_image = f'https://dlnqgsc0jr0k.cloudfront.net/{img}'
                news_obj.save()
                self.create_tag(content_text, news_obj)
                target.reason = ''

            target.is_active = True

        __create(target_url, entries)
        target.save()

    @staticmethod
    def create_tag(content_text: str, news_obj: News):
        tag_maps = []

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

    @staticmethod
    def news_check(title: str, content_text: str, page_url: str, target: str, source_site: str, featured_image: str):
        # only save the content that has img and content_text
        for key in DISALLOW_WORDS:
            if key in title:
                return True

        check_title = title.replace('【トピックス】', '')

        if content_text == '':
            return True

        try:
            exists = News.objects.filter(
                Q(title=check_title) | Q(url=page_url)
            ).exists()
        except Exception as e:
            return True
            print(
                f'This happend from collect news create on row 114 \n {e}'
            )

        if exists:
            return True

        top_two = News.objects.order_by(
            '-created_at'
        ).all()[:2]

        is_continuous = True
        for n in top_two:
            if n.site.pk != target.pk or n.source_site != source_site:
                is_continuous = False

        if is_continuous:
            return True

        featured_image = featured_image if featured_image is not None else ''
        if featured_image in ('', None):
            return True
