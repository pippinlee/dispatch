from django.conf.urls import patterns, include, url
from views import UbysseyTheme

theme = UbysseyTheme()

theme_urls = patterns('',
    url(r'^(?P<section>[-\w]+)/(?P<slug>[-\w]+)/?', theme.article, name='article'),
    url(r'^(?P<section>[-\w]+)/$', theme.section, name='section'),
    url(r'^$', theme.home, name='home'),
)
