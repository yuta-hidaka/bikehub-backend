        import json
from django.db.models import Q
from django.core.management.base import BaseCommand
from news.models import News, SourseSite
from urllib.parse import urlparse

class Command(BaseCommand):
    def handle(self, **options):
        
        sourse_site_list = SourseSite.objects.all()
        for sourse_site in sourse_site_list:

            filtered_sourse_site_list = SourseSite.objects.filter(
                name=sourse_site.name,
                sorce_url=sourse_site.sorce_url
            ).all()

            a = len(filtered_sourse_site_list)
            data_list = []
            site_list = []
            last_site = None
            if a > 1:
                for site in filtered_sourse_site_list:
                    print(site.name)
                    print(site.pk)
                    newss = News.objects.filter(source_site=site).all()
                    print(len(newss))
                    if len(newss) == 0:
                        site.delete()
                    else:
                        last_site = site
                        data_list.append(newss)

                if not last_site:
                    raise ValueError("site is noenennenen")
                for data in data_list:
                    for n in data:
                        site_list.append(n.source_site)
                        if n.source_site.pk != last_site.pk:
                            n.source_site = last_site
                            n.save()

                for s in site_list:
                    if last_site.pk != s.pk:
                        s.delete()


