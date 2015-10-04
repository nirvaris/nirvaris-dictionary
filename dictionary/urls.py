from django.conf.urls import url, include
from django.contrib import admin

from .views import WordEntryView, SearchView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),    
    url(r'^search$', SearchView.as_view()),
    url(r'^(?P<tags>.*)$', WordEntryView.as_view()),

]