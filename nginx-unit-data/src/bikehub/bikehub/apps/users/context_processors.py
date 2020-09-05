from django.contrib import admin


def admin_header_processor(request):
    site_header = getattr(admin.sites, 'site_header')
    index_title = getattr(admin.sites, 'index_title')
    site_title = getattr(admin.sites, 'site_title')

    return {
        "site_header": site_header,
        "site_header": index_title,
        "site_header": site_title
    }
