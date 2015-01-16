from django.contrib import admin
from django import forms
from dispatch.apps.content.models import Tag, Topic, Article, Section, Image, Video


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("short_headline",)}

    form = ArticleForm
    list_display = ('long_headline', 'updated_at')

    fieldsets = (
        ('Content', {
            'fields': ('long_headline', 'short_headline', 'content',)
        }),
        ('Basic', {
            'fields': ('published_at', 'section', 'importance', 'slug',)
        }),
        ('', {
            'fields': ('topics', 'tags', 'shares',)
        }),
        ('Media', {
            'fields': ('images', 'videos',)
        }),
        ('Developer', {
            'fields': ('snippets', 'scripts', 'stylesheets',)
        }),
    )

class ImageAdmin(admin.ModelAdmin):
    list_display = ('img', 'updated_at')

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'updated_at')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Section)
admin.site.register(Image, ImageAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Tag)
admin.site.register(Topic)
