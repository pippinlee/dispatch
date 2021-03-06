from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
from django.contrib.admin.views.decorators import staff_member_required

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^logout/?$', views.logout),
    url(r'^login/?$', views.login),
    url(r'^profile/?$', views.profile),
    url(r'^default/?$', include(admin.site.urls)),
    url(r'^users/$', views.users),
    url(r'^user/(\d*)/$', views.user_edit),
    url(r'^user/add/?$', views.user_add),
    url(r'^articles/$', views.articles),
    url(r'^article/(\d*)/$', views.article_edit),
    url(r'^article/delete/(\d*)/?$', views.article_delete),
    url(r'^article/add/(?P<section>[-\w]+)/?$', views.article_add),
    url(r'^article/add/?$', views.article_add),
    url(r'^section/edit/(\d*)/?$', views.section_edit),
    url(r'^section/add/?$', views.section_add),
    url(r'^section/(?P<section>[-\w]+)/?$', views.section),
    url(r'^sections/$', views.sections),
    url(r'^pages/$', views.pages),
    url(r'^page/edit/(?P<slug>[-\w]+)/?$', views.page_edit),
)
