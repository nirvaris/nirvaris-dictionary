from django.contrib import admin

from .models import WordEntry, MetaTag, Tag, Comment, Language, Picture

admin.site.register(WordEntry)
admin.site.register(MetaTag)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Language)
admin.site.register(Picture)