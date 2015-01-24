__author__ = 'Steven Richards'
from django.contrib.auth import get_user_model
from django.db.models import Q
from dispatch.apps.content.models import Article, Tag, Image, Attachment, Section
from dispatch.apps.core.models import Person
from rest_framework import viewsets
from rest_framework.response import Response
from dispatch.apps.api.serializers import UserSerializer, ArticleSerializer, ImageSerializer, AttachmentSerializer, TagSerializer, PersonSerializer, SectionSerializer, SearchSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

class ImageViewSet(viewsets.ModelViewSet):
    model = Image
    serializer_class = ImageSerializer

    def get_queryset(self):
        queryset = Image.objects.all()
        q = self.request.QUERY_PARAMS.get('q', None)
        if q is not None:
            queryset = queryset.filter(caption__icontains=q)
        return queryset


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class SearchViewSet(viewsets.ViewSet):
    def list(self, request):
        q = self.request.GET.get("q")
        if not q:
            return Response({})

        querysets = {
            "articles": Article.objects.filter(
                #Q(authors__full_name__icontains=q) |
                Q(long_headline__icontains=q)
            ),
            "sections": Section.objects.filter(
                name__icontains=q
            )
        }
        serializer = SearchSerializer(querysets, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        return self.list(request)
