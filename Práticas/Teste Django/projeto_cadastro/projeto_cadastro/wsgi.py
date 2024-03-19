# Parte do código destinada à aplicações que precisam de suporte de WSGI

"""
WSGI config for projeto_cadastro project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_cadastro.settings')

application = get_wsgi_application()
