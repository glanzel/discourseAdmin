"""
WSGI config for dsso project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys, logging


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dsso.settings')
# uncomment if you use a python venv and modify path so that its point to your env site-packages
#sys.path.append(os.path.join(sys.path[0], 'env', 'lib', 'python3.9', 'site-packages')) 
#print(sys.path)

application = get_wsgi_application()
