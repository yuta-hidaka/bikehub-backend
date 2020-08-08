"""
WSGI config for bikehub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

# ############## for remote debug
# import ptvsd
# try:
#     ptvsd.enable_attach(address=('0.0.0.0', 9090))
#     pass
# except:
#     pass

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikehub.settings')

application = get_wsgi_application()
