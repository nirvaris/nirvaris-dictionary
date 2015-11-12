from django.contrib import admin

from .models import WordEntry, Tag, Comment, Language, Picture, WordFunction, WordType


#class WordEntryAdmin(admin.ModelAdmin):
#    list_filter = ('tags','author','template')
#    list_display = ('word','relative_url','short_description','meaning','scientific_name','curiosities','phonetics','audio_file','template','access_count','created')
#    search_fields = ['word','relative_url','short_description','meaning','scientific_name','curiosities']
  
admin.site.register(WordEntry)


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
admin.site.register(Language)
admin.site.register(Picture)
admin.site.register(WordFunction)
