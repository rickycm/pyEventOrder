__author__ = 'Aston'
# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import sys

import os


## assuming your django settings file is at '/home/whitemay/mysite/settings.py'
path = '/home/ec2-user/src/pyeventorder'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'pyEventOrder.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
