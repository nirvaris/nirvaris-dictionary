from django.conf.urls import url

from .views import WordEntryView, SearchView

urlpatterns = [
    url(r'^search$', SearchView.as_view()),
    url(r'^(?P<tags>.*)$', WordEntryView.as_view()),

]