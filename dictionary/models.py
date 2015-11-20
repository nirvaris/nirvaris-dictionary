from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    display = models.CharField(max_length=200, unique=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=70, unique=True)
    location = models.CharField(max_length=70)
    is_tribal = models.BooleanField(default=True)
    def __str__(self):
        return self.name

# Grammar function, like verb, adjetive
class WordClass(models.Model):
    name = models.CharField(max_length=255, unique=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    def __str__(self):
        return self.name    
        
class WordContent(models.Model):
    author = models.ForeignKey(User, related_name='word_entries_content') 
    content = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True) 
    def __str__(self):
        return self.content

class Picture(models.Model):
    description = models.CharField(max_length=155)    
    file_name = models.CharField(max_length=255)
    display_order = models.PositiveSmallIntegerField(default=0)
    word_content = models.ForeignKey(WordContent, related_name='pictures')
    def __str__(self):
        return self.description + ' - ' + self.file_name

class WordEntry(models.Model):
    author = models.ForeignKey(User, related_name='word_entries')
    relative_url = models.CharField(max_length=155, unique=True, null=False)
    word = models.CharField(max_length=100, null=False)
    short_description = models.CharField(max_length=155, null=False)
    languages = models.ManyToManyField(Language, related_name='word_entries')
    word_classes = models.ManyToManyField(WordClass, related_name='word_entries')
    audio_file = models.CharField(max_length=255, null=True, blank=True)
    phonetics = models.CharField(max_length=255, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='tags')
    template = models.CharField(max_length=50, null=False, default='word-entry-default.html')
    is_published = models.BooleanField(default=False)
    access_count = models.BigIntegerField(default=0, null=False)
    word_content = models.ForeignKey(WordContent, related_name='word_entries',null=False) 
    words_related = models.ManyToManyField('WordEntry', related_name='word_related_to')
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.word + ' (url: /' + self.relative_url + ')' 

    
class Comment(models.Model):
    author = models.ForeignKey(User, null=True, related_name='word_entry_comments') 
    word_entry = models.ForeignKey(WordEntry, related_name='word_entry_comments') 
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)        
    def __str__(self):
        if self.author:
            return self.author.get_full_name()
        return 'Anonymous'
        
