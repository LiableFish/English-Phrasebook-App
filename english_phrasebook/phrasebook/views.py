from django.shortcuts import render
from django.conf import settings
from .permissions import CheckSecretAPI

from .models import Category, Theme, Level, Word
from .serializers import CategorySerializer, ThemeDetailSerializer, \
    ThemeListSerializer, LevelSerializer, WordDetailSerializer

from rest_framework import generics


def index(request):
    context = {}
    return render(request, 'phrasebook/index.html', context)


class CategoriesList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    if not settings.DEBUG:
        permission_classes = [CheckSecretAPI]


class LevelsList(generics.ListAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

    if not settings.DEBUG:
        permission_classes = [CheckSecretAPI]


class ThemesList(generics.ListAPIView):
    serializer_class = ThemeListSerializer

    if not settings.DEBUG:
        permission_classes = [CheckSecretAPI]

    def get_queryset(self):
        """
        return themes by filtering against a 'category' and 'level' optional query parameters in the URL.
        """
        queryset = Theme.objects.all()
        category = self.request.query_params.get('category', None)
        level = self.request.query_params.get('level', None)
        if category is not None:
            queryset = queryset.filter(category_id=category)
        if level is not None:
            queryset = queryset.filter(level_id=level)
        return queryset


class ThemeDetail(generics.RetrieveAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeDetailSerializer

    if not settings.DEBUG:
        permission_classes = [CheckSecretAPI]


class WordDetail(generics.RetrieveAPIView):
    queryset = Word.objects.all()
    serializer_class = WordDetailSerializer

    if not settings.DEBUG:
        permission_classes = [CheckSecretAPI]
