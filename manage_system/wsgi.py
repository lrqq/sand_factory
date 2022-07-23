"""
WSGI config for manage_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


# 引入global_var
from . import mqtt_functions
import manage_system.gloabl_var as global_var

mqtt_functions.mqtt_run()
global_var._init()
# global_var end

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manage_system.settings')

application = get_wsgi_application()
