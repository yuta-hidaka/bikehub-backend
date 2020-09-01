import feedparser
from news.models import *
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.parse import urljoin
from .find_img import FindImg
from .find_tag import FindTag
from .find_content import FindContents
import pandas as pd


class CollectNews():
    @staticmethod
    def collect_news():
        all_target = TargetSite.objects.all()
        fi = FindImg()
        fc = FindContents()

        # get each url
        for target in all_target:
            target_url = target.rss_url
            tag_name = target.content_tag.tag_type
            tag_name_class = target.content_tag.tag_class_name
            tag_name_id = target.content_tag.tag_id_name
            is_active = False
            feeds = feedparser.parse(target.rss_url)
            if(len(feeds['entries'])):
                is_active = True
                # get each contents
                for entrie in feeds['entries']:
                    tag_maps = []
                    page_url = entrie['links'][0]['href']
                    title = entrie['title']
                    featured_image = None
                    content_text = None
                    featured_image = fi.find_img(
                        entrie, feeds, page_url, target_url
                    )
                    content_text = fc.find_contents(
                        page_url, tag_name, tag_name_class, tag_name_id
                    )
                    # create summary
                    tmp_summary = [
                        a for a in content_text[:300].split() if a != ''
                    ]

                    summary = '\n'.join(tmp_summary[3:])
                    # only save the content that has img and content_text
                    if featured_image and content_text:
                        # if same titile are exsist skip that news
                        result = News.objects.filter(title=title).first()
                        if result is None:
                            # create news contens
                            news_obj, created = News.objects.get_or_create(
                                title=title,
                                summary=summary,
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

                                SubCategoryTagMap.objects.bulk_create(tag_maps)
                                target.reason = ''
                                
            else:
                target.reason = 'can not find feeds["entries"]'

                target.is_active = is_active
                target.save()

    def create_news(self):
        all_target = TargetSite.objects.all().filter(name="").filter(url="").values()
        for target in all_target:
            parsed_url = urlparse(target['rss_url'])
            print(parsed_url)

    def create_tags(self, news_title):
        print('')
