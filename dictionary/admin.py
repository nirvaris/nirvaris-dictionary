from django.contrib import admin

from .models import WordEntry, MetaTag, Tag, Comment, Language, Picture

admin.site.register(WordEntry)
class MetaTagAdmin(admin.ModelAdmin):
    list_filter = ('word_entry','name','property','content')
    list_display = ('word_entry','name','property','content')
    search_fields = ['name','property','content']
    
admin.site.register(MetaTag, MetaTagAdmin)


class TagAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('name',)
    search_fields = ['name',]
    
admin.site.register(Tag,TagAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_filter = ('word_entry','author','content','is_approved','created')
    list_display = ('word_entry','author','content','is_approved')
    list_editable = ('is_approved',)
    search_fields = ['content']

admin.site.register(Comment, CommentAdmin)

admin.site.register(Language)
admin.site.register(Picture)