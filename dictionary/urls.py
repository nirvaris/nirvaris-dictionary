from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required


from .views import WordEntryView, SearchView, UploadCSVView, DemoSearchFormView, UploadTagCSVView, UploadLanguageCSVView, DownloadImportLogView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/', include('n_profile.urls')),
    url(r'^search-form-tag$', DemoSearchFormView.as_view(), name='search-form-tag'),
    url(r'^search$', SearchView.as_view(), name='search'),
    url(r'^upload-csv$', login_required(UploadCSVView.as_view()), name='upload-csv'),
    url(r'^upload-tag-csv$', login_required(UploadTagCSVView.as_view()), name='upload-tag-csv'),
    url(r'^upload-language-csv$', login_required(UploadLanguageCSVView.as_view()), name='upload-language-csv'),
    url(r'^download-log$', login_required(DownloadImportLogView.as_view()), name='download-log'),

    url(r'^(?P<tags>.*)$', WordEntryView.as_view(), name='tag-letter'),
]
