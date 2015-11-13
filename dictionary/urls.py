from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required


from .views import WordEntryView, SearchView, UploadCSV, SearchFormTag, UploadTagCSV, UploadLanguageCSV, DownloadImportLog


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),    
    url(r'^search-form-tag$', SearchFormTag.as_view(), name='search-form-tag'),
    url(r'^search$', SearchView.as_view(), name='search'),
    url(r'^upload-csv$', login_required(UploadCSV.as_view()), name='upload-csv'),
    url(r'^upload-tag-csv$', login_required(UploadTagCSV.as_view()), name='upload-tag-csv'),
    url(r'^upload-language-csv$', login_required(UploadLanguageCSV.as_view()), name='upload-language-csv'),
    url(r'^download-log$', login_required(DownloadImportLog.as_view()), name='download-log'),        
    url(r'^(?P<tags>.*)$', WordEntryView.as_view()),
]