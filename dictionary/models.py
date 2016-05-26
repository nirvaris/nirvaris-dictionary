from django.contrib.auth.models import User
from django.db import models

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'gallery/{0}'.format(filename)
    #return 'gallery/{0}/{1}'.format(instance.url, filename)

class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    display = models.CharField(max_length=200, unique=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class LanguageType(models.Model):
    name = models.CharField(max_length=70, unique=True)
    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=70, unique=True)
    parent = models.ForeignKey('Language', related_name='language_parent', null=True, blank=True)
    language_type = models.ForeignKey(LanguageType, related_name='languages', null=True, blank=True)
    location_name = models.CharField(max_length=70, null=True, blank=True)
    location_latitude = models.PositiveSmallIntegerField(default=0)
    location_longitude = models.PositiveSmallIntegerField(default=0)
    is_tribal = models.BooleanField(default=True)
    def __str__(self):
        return self.name

# Grammar function, like verb, adjetive
class WordClass(models.Model):
    name = models.CharField(max_length=255, unique=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    def __str__(self):
        return self.name

class WordContentReference(models.Model):
    reference = models.CharField(max_length=1024, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.content

class WordContent(models.Model):
    author = models.ForeignKey(User, related_name='word_contents')
    references = models.ManyToManyField(WordContentReference, related_name='word_contents')
    content = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.content

class Picture(models.Model):
    description = models.CharField(max_length=155)
    full = models.ImageField(upload_to=user_directory_path, null=True, max_length=1024)
    small = models.ImageField(upload_to=user_directory_path, null=True, max_length=1024)
    tinny = models.ImageField(upload_to=user_directory_path, null=True, max_length=1024)
    display_order = models.PositiveSmallIntegerField(default=0)
    word_content = models.ForeignKey(WordContent, related_name='pictures')
    def __str__(self):
        return self.description

class WordEntry(models.Model):
    author = models.ForeignKey(User, related_name='word_entries')
    relative_url = models.CharField(max_length=155, unique=True, null=False)
    word = models.CharField(max_length=100, null=False)
    short_description = models.CharField(max_length=255, null=False)
    languages = models.ManyToManyField(Language, related_name='word_entries')
    word_classes = models.ManyToManyField(WordClass, related_name='word_entries')
    audio_file = models.CharField(max_length=255, null=True, blank=True)
    phonetics = models.CharField(max_length=255, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='tags')
    template = models.CharField(max_length=50, null=False, default='word-entry-default.html')
    is_published = models.BooleanField(default=False)
    access_count = models.BigIntegerField(default=0, null=False)
    word_content = models.ForeignKey(WordContent, related_name='word_entries',null=True, blank=True)
    words_related = models.ManyToManyField('WordEntry', blank=True, related_name='word_related_to')
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def thumb(self):
        picture = self.word_content.pictures.order_by('display_order').first()
        if picture and picture.tinny:
            return picture.tinny.url
        return '/static/image/no_image_tinny.png'

    def __str__(self):
        return self.word + ' (url: /' + self.relative_url + ')'


class WordComment(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, related_name='word_entry_comments')
    author_ip = models.GenericIPAddressField(null=True, blank=True)
    word_entry = models.ForeignKey(WordEntry, related_name='word_entry_comments')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    def __str__(self):
        if self.author:
            return self.author.get_full_name()
        return 'Anonymous'
