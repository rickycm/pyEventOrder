# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from pyEventOrderWeb import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'pyEventOrder.views.home', name='home'),
    # url(r'^pyEventOrder/', include('pyEventOrder.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'^$', 'pyEventOrderWeb.views.index'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
    (r'^login-form/$', views.login_form),
    (r'^accounts/register/$', 'pyEventOrderWeb.views.register'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/$', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
    (r'^list_events/$', views.list_events),
    (r'^add_event/$', views.add_event),
    (r'^add_event2/$', views.add_event2),
    url(r'^setting/$', views.setting),
    (r'^message/$', views.message),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^(?P<url>.*)$', 'flatpage'),
)

