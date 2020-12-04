import datetime
import os
import xml.etree.cElementTree as ET

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from news.models import News


def registerSiteMaps(base_url: str, directorys: list) -> object:
    root = ET.Element('urlset')
    root.attrib['xmlns:xsi'] = "http://www.w3.org/2001/XMLSchema-instance"
    root.attrib['xsi:schemaLocation'] = "http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
    root.attrib['xmlns'] = "http://www.sitemaps.org/schemas/sitemap/0.9"

    base_sites = ('fc', '')
    for base_site in base_sites:
        directorys.append(base_site)

    for directory in directorys:
        dt = datetime.datetime.now().strftime("%Y-%m-%d")
        doc = ET.SubElement(root, "url")
        ET.SubElement(doc, "loc").text = f'{base_url}/{directory}'
        ET.SubElement(doc, "lastmod").text = dt
        ET.SubElement(doc, "changefreq").text = "daily"
        ET.SubElement(doc, "priority").text = "1.0"

    tree = ET.ElementTree(root)
    tree.write('/code/static/sitemap.xml', encoding='utf-8', xml_declaration=True)

    return tree


@login_required
def site_map(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename="sitemap.xml"'

    news_ids = [f'article/{news.news_id}' for news in News.objects.all()]
    base_url = "https://web.bikehub.app"

    registerSiteMaps(base_url, news_ids)

    # return response
    with open('/code/static/sitemap.xml', 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="text/xml")
        response['Content-Disposition'] = 'attachment; filename="sitemap.xml"'
        os.remove('/code/static/sitemap.xml')
        return response
