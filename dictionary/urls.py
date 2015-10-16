from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from .views import WordEntryView, SearchView, UploadCSV

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),    
    url(r'^search$', SearchView.as_view(), name='search'),
    url(r'^upload-csv$', login_required(UploadCSV.as_view()), name='upload-csv'),    
    url(r'^(?P<tags>.*)$', WordEntryView.as_view()),
]