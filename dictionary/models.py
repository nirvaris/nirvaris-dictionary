from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class WordEntry(models.Model):
    author = models.ForeignKey(User, related_name='word_entries') 
    relative_url = models.CharField(max_length=155, unique=True, null=False)
    title = models.CharField(max_length=70, null=False) 
    word = models.CharField(max_length=100, null=False)
    languages = models.ManyToManyField('Language', related_name='word_entries')
    short_description = models.CharField(max_length=155)
    scientific_name = models.CharField(max_length=255, null=True, blank=True)
    audio_file = models.CharField(max_length=255, null=True, blank=True)
    phonetics = models.CharField(max_length=255, null=True, blank=True)
    meaning = models.TextField()
    curiosities = models.TextField(null=False, blank=True)
    tags = models.ManyToManyField('Tag', related_name='tags')
    template = models.CharField(max_length=50, null=False,default='word-entry-default.html')
    access_count = models.BigIntegerField(default=0,null=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True) 
               
    def __str__(self):
        return self.title + ' (url: /' + self.relative_url + ')' 

class Picture(models.Model):
    description = models.CharField(max_length=155)    
    full_file_name = models.CharField(max_length=255, unique=True)
    small_file_name = models.CharField(max_length=255, unique=True) 
    tiny_file_name = models.CharField(max_length=255, unique=True)       
    word_entry = models.ForeignKey('WordEntry')
    
class MetaTag(models.Model):
    name = models.CharField(max_length=70)
    property = models.CharField(max_length=70)
    content  = models.CharField(max_length=70)
    word_entry = models.ForeignKey('WordEntry')

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
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
        
class Language(models.Model):
    name = models.CharField(max_length=70)
    def __str__(self):
        return self.name
   