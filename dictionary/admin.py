from django.contrib import admin

from .models import WordEntry, Tag, Comment, Language, Picture, WordClass, WordContent

def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)

make_published.short_description = "Mark selected as published"

class WordEntryAdmin(admin.ModelAdmin):
    list_filter = ('languages','word_classes','words_related','tags','author','template')
    list_display = ('word','relative_url','short_description','is_published','phonetics','audio_file','template','access_count','created','word_content')
    search_fields = ['word','relative_url','short_description','word_content__content']
    list_editable = ('is_published',)
    actions = [make_published]

admin.site.register(WordEntry,WordEntryAdmin)


class TagAdmin(admin.ModelAdmin):
    list_filter = ('name','display',)
    list_display = ('name','display',)
    search_fields = ['name','display']

admin.site.register(Tag,TagAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_filter = ('word_entry','author','content','is_approved','created')
    list_display = ('word_entry','author','content','is_approved')
    list_editable = ('is_approved',)
    search_fields = ['content']

admin.site.register(Comment, CommentAdmin)

class WordContentAdmin(admin.ModelAdmin):
    search_fields = ['content']


admin.site.register(WordContent, WordContentAdmin)

class PictureAdmin(admin.ModelAdmin):
    search_fields = ['file_name', 'description']

admin.site.register(Picture,PictureAdmin)

admin.site.register(Language)

admin.site.register(WordClass)
