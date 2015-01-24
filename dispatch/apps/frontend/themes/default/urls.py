from django.conf.urls import patterns, include, url

from views import DefaultTheme

theme = DefaultTheme()

theme_urls = patterns('',
    url(r'^search', theme.search),
    url(r'^(?P<section>[-\w]+)/(?P<slug>[-\w]+)/', theme.article),
    url(r'^', theme.home),
)
