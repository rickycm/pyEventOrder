# coding=utf-8
from django.conf.urls import patterns, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from pyEventOrderWeb import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'pyEventOrder.views.home', name='home'),
    # url(r'^pyEventOrder/', include('pyEventOrder.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^$', 'pyEventOrderWeb.views.index'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
    #(r'^login/$', views.check_auth),
    (r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
    (r'^login-form/$', views.login_form),
    (r'^accounts/register/$', 'pyEventOrderWeb.views.register'),
    (r'^accounts/logout/$', views.logout_view),
    (r'^accounts/$', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
    (r'^list_events/$', views.list_events),
    (r'^add_event/$', views.add_event),
    (r'^updateevent/$', views.updateEvent),
    (r'^showevent/$', views.showEvent),
    (r'^joinevent/$', views.joinEvent),
    (r'^checkmail/$', views.checkEmail),
    (r'^jslogin/$', views.jslogin),
    (r'^jsregister/$', views.jsregister),
    (r'^index/$', views.index),
    (r'^setting/$', views.setting),
    (r'^message/$', views.message),
    (r'^oauth/$', views.oauth),
    (r'^welcome/$', views.welcome),
    (r'^test/$', views.test),
    (r'^tinymce/', include('tinymce.urls')),
    (r'', include('jqmFlatPages.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

#urlpatterns += patterns('django.contrib.flatpages.views',
#    (r'^pages/', include('django.contrib.flatpages.urls')),
#)

