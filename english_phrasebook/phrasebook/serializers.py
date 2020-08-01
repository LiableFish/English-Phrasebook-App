from rest_framework import serializers
from .models import Category, Theme, Level, Word


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name', 'code']


class ThemeDetailSerializer(serializers.ModelSerializer):
    class WordRelatedSerializer(serializers.ModelSerializer):
        class Meta:
            model = Word
            fields = ['id', 'name']

    words = WordRelatedSerializer(many=True, read_only=True)

    class Meta:
        model = Theme
        fields = ['id', 'category', 'level', 'name', 'photo', 'words']


class ThemeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'category', 'level', 'name', 'photo']


class WordDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'name', 'translation', 'transcription', 'example', 'sound']
