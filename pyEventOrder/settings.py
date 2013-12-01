# -*- coding: utf-8 -*-
# Django settings for pyEventOrder project.
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
    ('Ricky Chi', 'rickycm@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'whitemay$pyeventorder',
        'USER': 'whitemay',
        'PASSWORD': '1qazxsw2',
        'HOST': 'mysql.server',
        'PORT': '',
    },
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'
#STATIC_URL = os.path.join( os.path.dirname(__file__), '../templates/static/')

# Additional locations of static files
STATICFILES_DIRS = (
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
#os.path.join(STATIC_ROOT, 'twitter_bootstrap'),
#os.path.join(STATIC_ROOT, 'font_awesome'),
    os.path.join(PROJECT_ROOT, 'resources'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'jq+la0+66bkt)@8)6xt3ds!426u^q)$&9n=%fp-twfskf$i_8$'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

APPEND_SLASH = True

AUTHENTICATION_BACKENDS = (
    'pyEventOrderWeb.auth.OAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = "/login/"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'wx-eventorder',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 12096000

ROOT_URLCONF = 'pyEventOrder.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'pyEventOrder.wsgi.application'

#TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\','/'),)
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'admin_bootstrap/templates').replace('\\', '/'),
    os.path.join(PROJECT_ROOT, 'templates').replace('\\', '/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.flatpages',
    'crispy_forms',
    'admin_bootstrap',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'south',
    # 引入对bootstrap3的支持，由于admin界面所采用的是2.x版本，因此需要加以区别
    'jquery',
    'bootstrap3',
    'awesome_bootstrap',
    'dh5bp',
    'dh5mbp',
    'bootstrap3_datetime',
    'pyEventOrderWeb',
    #'djWeixinApp',
    'rest_framework',
    'restComments',
)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    #'DEFAULT_PARSER_CLASSES': (
        #'rest_framework.parsers.JSONParser',
        #'rest_framework.parsers.FormParser',
        #'rest_framework.parsers.MultiPartParser',
    #)
}

CRISPY_TEMPLATE_PACK = 'uni_form'

# 覆盖bootstrap3中间的缺省值，用来通过awesome_bootstrap载入静态文件
# dist子目录下的bootstrap为版本3，从而可以避免版本上的混乱
BOOTSTRAP3 = {
    'include_jquery': False,
    'jquery_url': '/static/admin/js/jquery.min.js',
    'base_url': '/static/twitter_bootstrap/dist/',
    'theme_url': '/static/twitter_bootstrap/dist/css/bootstrap-theme.min.css',
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.dev': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
