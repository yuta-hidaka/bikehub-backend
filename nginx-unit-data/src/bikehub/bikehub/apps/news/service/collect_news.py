import feedparser
from news.models import *
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.parse import urljoin
from .find_img import FindImg
from .find_tag import FindTag
from .find_content import FindContents
import pandas as pd
from django.db.models import Q
from concurrent.futures import ThreadPoolExecutor


class CollectNews():
    def collect_news(self):
        target_sites = TargetSite.objects.all()
        # with ThreadPoolExecutor() as w:
        #     w.map(self.collect, target_sites)
        for i in target_sites:
            self.collect(i)

    def collect(self, target):
        fi = FindImg()
        fc = FindContents()
        target_url = target.rss_url
        tag_name = target.content_tag.tag_type
        tag_name_class = target.content_tag.tag_class_name
        tag_name_id = target.content_tag.tag_id_name
        summary = ''
        is_active = False
        feeds = feedparser.parse(target_url)

        try:
            entries = feeds['entries']
            print(target_url)
            print(f'記事の長さは　：　{len(entries)}')
            # print(feeds['entries'])
            if(len(entries)):
                # get each contents
                for entriy in entries:
                    tmp_summary = ''
                    tag_maps = []
                    page_url = entriy['links'][0]['href']
                    title = entriy['title']
                    featured_image = None
                    content_text = None
                    featured_image = fi.find_img(
                        entriy, feeds, page_url, target_url
                    )
                    content_text = fc.find_contents(
                        page_url, tag_name, tag_name_class, tag_name_id
                    )
                    print('content_text')
                    print(content_text[:10])

                    if content_text != '':
                        # create summary
                        tmp_summary = [
                            a for a in content_text.split() if a != '' and not len(a) < 20
                        ]

                    try:
                        check_title = title[:15]
                    except:
                        check_title = title

                    summary = '\n'.join(tmp_summary)
                    summary = summary[:300]
                    # only save the content that has img and content_text
                    if content_text != '':
                        if '【トピックス】' in title:
                            Query = (
                                Q(title__contains=check_title[:10])
                            )
                        else:
                            Query = (
                                Q(title__contains='【トピックス】')
                                &
                                Q(title__contains=check_title)
                            )

                        # if same titile are exsist skip that news

                        exists = News.objects.filter(
                            Query |
                            Q(
                                url=page_url
                            ) |
                            Q(
                                title=title
                            )
                        ).exists()
                        print(exists)

                        if not exists:
                            topThree = News.objects.order_by(
                                '-created_at'
                            ).all()[:3]

                            IsContinuous = True
                            for n in topThree:
                                if n.site.pk != target.pk:
                                    IsContinuous = False

                            if not IsContinuous:
                                featured_image = featured_image if featured_image is not None else ''
                                # create news contens
                                news_obj, created = News.objects.get_or_create(
                                    title=title,
                                    summary=summary[:300],
                                    url=page_url,
                                    site=target,
                                    featured_image=featured_image
                                )

                                if created:
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
                is_active = True

            else:
                target.reason = 'can not find feeds["entries"]'
        except Exception as e:
            print(e)
            target.reason = str(e)

        target.is_active = is_active
        target.save()

    # def create_news(self):
    #     all_target = TargetSite.objects.all().filter(name="").filter(url="").values()
    #     for target in all_target:
    #         parsed_url = urlparse(target['rss_url'])
    #         print(parsed_url)

    # def create_tags(self, news_title):
    #     print('')
