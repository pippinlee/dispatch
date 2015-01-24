__author__ = 'Steven Richards'
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from dispatch.apps.content.models import Article, Tag, Image, Attachment, Section
from dispatch.apps.core.models import Person
from rest_framework import serializers

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    thumb = serializers.CharField(source='get_thumbnail_url', read_only=True)

    class Meta:
        model = Image
        fields = ('id', 'img', 'url', 'thumb')

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())
    image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())

    class Meta:
        model = Attachment
        fields = ('id', 'article', 'image', 'caption')

class SectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Section
        fields = ('name',)


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ('long_headline',
                  'short_headline',
                  'section',
                  'is_published',
                  'published_at',
                  'slug',
                  'content')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('url', 'email')

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('first_name','last_name','user','roles')


class SearchSerializer(serializers.BaseSerializer):
    def __init__(self, *args, **kwargs):
        ctx = kwargs.get("context")
        self.request = ctx.get("request") if ctx else None

        super(SearchSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        """
        We expect `obj` to be a dict of querysets, eg.
        {
            "articles": <queryset>,
            "sections": <queryset>,
            ...
        }
        """
        output = {}
        for key, qset in obj.items():
            output[key] = []
            if key is "articles":
                output[key] = ArticleSerializer(
                    obj[key],
                    many=True,
                    context={"request": self.request}).data
            elif key is "sections":
                output[key] = SectionSerializer(
                    obj[key],
                    many=True,
                    context={"request": self.request}).data

        return output
