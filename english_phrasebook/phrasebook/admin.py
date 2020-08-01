from django.contrib import admin
from .models import Category, Theme, Level, Word

admin.site.register(Category, readonly_fields=['icon_tag'])
admin.site.register(Theme, readonly_fields=['photo_tag'])
admin.site.register(Level)
admin.site.register(Word, fields=['theme', 'name', 'translation', 'transcription', 'example', 'sound', 'sound_tag'],
                    readonly_fields=['transcription', 'sound_tag'])
