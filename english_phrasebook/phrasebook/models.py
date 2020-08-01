import eng_to_ipa as ipa
import magic
import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileValidator(object):
    """
    Validate max/min size and content type of files using python-magic module.
    """
    error_messages = {
        'max_size': ('Ensure this file size is not greater than %(max_size)s.'
                     ' Your file size is %(size)s.'),
        'min_size': ('Ensure this file size is not less than %(min_size)s. '
                     'Your file size is {size}.'),
        'content_type': 'Files of type %(content_type)s are not supported.',
    }

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size),
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'],
                                  'max_size', params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.min_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['min_size'],
                                  'min_size', params)

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            if content_type not in self.content_types:
                params = {'content_type': content_type}
                raise ValidationError(self.error_messages['content_type'],
                                      'content_type', params)

    def __eq__(self, other):
        return \
            isinstance(other, FileValidator) and \
            self.max_size == other.max_size and \
            self.min_size == other.min_size and \
            self.content_types == other.content_types


@deconstructible
class PathWithName:
    """
    Creates a path for 'uploads_to' param in FileField using an instance name and root directory.
    The root directory is supposed to be correspond to the model FileField name.
    """

    def __init__(self, root):
        self.root = root

    def __call__(self, instance, filename):
        return os.path.join(self.root, instance.name, filename)


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    icon = models.ImageField(upload_to=PathWithName('icons'), blank=True, null=True)

    def icon_tag(self):
        if self.icon:
            return mark_safe(f'<img src="{self.icon.url}" width="100" height="100" />')
        else:
            return 'Icon has not downloaded yet'

    icon_tag.short_description = 'Icon image'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('сategory')
        verbose_name_plural = _('categories')


class Level(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Theme(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    photo = models.ImageField(upload_to=PathWithName('photos'), blank=True, null=True)

    def photo_tag(self):
        if self.photo:
            return mark_safe(f'<img src="{self.photo.url}" width="100" height="100" />')
        else:
            return 'Photo has not downloaded yet.'

    photo_tag.short_description = 'Photo image'

    def __str__(self):
        return self.name


class Word(models.Model):
    validate_sound = FileValidator(max_size=52428800, content_types=('audio/mpeg', 'audio/vnd.wave', 'audio/ogg'))

    theme = models.ForeignKey(Theme, related_name='words', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='phrase', unique=True)
    translation = models.CharField(max_length=200)
    example = models.CharField(max_length=200)
    sound = models.FileField(upload_to=PathWithName('sounds'), validators=[validate_sound],
                             blank=True, null=True,
                             help_text='Allowed type - .mp3, .wav, .ogg')

    def transcription(self):
        if self.name:
            return ipa.convert(self.name)
        else:
            return 'Phrase has not be added yet'

    def sound_tag(self):
        if self.sound:
            return mark_safe(f'<audio src="{self.sound.url}" controls>Your browser does not '
                             f'support the <code>audio</code> element.</audio>')
        else:
            return 'Audio has not downloaded yet.'

    sound_tag.short_description = 'Audio sample'

    def __str__(self):
        return self.name


def auto_delete_file_on_delete(model, filename):
    """
    Deletes file and corresponding instance directory from filesystem
    when corresponding model object is deleted.
    """

    @receiver(models.signals.post_delete, sender=model)
    def auto_delete(sender, instance, **kwargs):
        file = getattr(instance, filename)
        if file:
            if os.path.isfile(file.path):
                os.remove(file.path)
                path_with_name = PathWithName(filename + 's')
                instance_file_directory = os.path.join(settings.MEDIA_ROOT, path_with_name(instance, ''))
                if os.path.isdir(instance_file_directory) and not os.listdir(instance_file_directory):
                    os.rmdir(instance_file_directory)

    return auto_delete


def auto_delete_file_on_change(model, filename):
    """
    Deletes old file from filesystem when corresponding model object is updated with new file. If new file is empty
    (see 'clear' in model change page) then corresponding instance directory will also be deleted.
    """

    @receiver(models.signals.pre_save, sender=model)
    def auto_delete(sender, instance, **kwargs):
        if not instance.pk:
            return False

        try:
            old_file = getattr(sender.objects.get(pk=instance.pk), filename)
        except model.DoesNotExist:
            return False

        new_file = getattr(instance, filename)
        if not old_file == new_file:
            if old_file and os.path.isfile(old_file.path):
                os.remove(old_file.path)
                if not new_file:
                    path_with_name = PathWithName(filename + 's')
                    instance_file_directory = os.path.join(settings.MEDIA_ROOT, path_with_name(instance, ''))
                    if os.path.isdir(instance_file_directory) and not os.listdir(instance_file_directory):
                        os.rmdir(instance_file_directory)

    return auto_delete


auto_delete_icon_on_delete = auto_delete_file_on_delete(model=Category, filename='icon')
auto_delete_icon_on_change = auto_delete_file_on_change(model=Category, filename='icon')

auto_delete_photo_on_delete = auto_delete_file_on_delete(model=Theme, filename='photo')
auto_delete_photo_on_change = auto_delete_file_on_change(model=Theme, filename='photo')

auto_delete_sound_on_delete = auto_delete_file_on_delete(model=Word, filename='sound')
auto_delete_sound_on_change = auto_delete_file_on_change(model=Word, filename='sound')
