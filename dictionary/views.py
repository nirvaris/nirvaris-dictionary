import os
import pdb

from threading import Thread

from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from django.views.generic import TemplateView

from django.utils.encoding import smart_str

from django.views.generic.base import View
# Create your views here.

from .csv_things import import_csv, import_tag_csv, import_language_csv, import_comments_csv, DICTIONARY_CSV_FIELDS, TAG_CSV_FIELDS, LANGUAGE_CSV_FIELDS
from .forms import WordCommentForm, SearchForm, UploadCSVForm
from .models import WordEntry

NV_DICTIONARY_GALLERY_EMPTY_IMAGE = 'static/image/empty-image.jpg'

if hasattr(settings, 'NV_THEME_GALLERY_EMPTY_IMAGE'):
    if settings.NV_THEME_GALLERY_EMPTY_IMAGE:
        NV_DICTIONARY_GALLERY_EMPTY_IMAGE = settings.NV_THEME_GALLERY_EMPTY_IMAGE


NV_SITE_URL = 'http://localhost:8080/'

if hasattr(settings, 'NV_SITE_URL'):
    if settings.NV_SITE_URL:
        NV_SITE_URL = settings.NV_SITE_URL

NV_DICTIONARY_URL = 'dictionary'

if hasattr(settings, 'NV_DICTIONARY_URL'):
    if settings.NV_DICTIONARY_URL:
        NV_DICTIONARY_URL = settings.NV_DICTIONARY_URL



class DownloadImportLogView(View):

    def get(self, request):
        log_file = open(request.session['log_file_path'])
        #pdb.set_trace()
        response = HttpResponse(log_file, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('import-log.log.txt')

        return response

class UploadCommentsCSVView(View):

    def get(self, request):
        form = UploadCSVForm()
        data_context = {'upload_form':form, 'mapped_fields': LANGUAGE_CSV_FIELDS}
        return render(request,'upload-comments-csv-form.html', data_context)

    def post(self, request):

        form = UploadCSVForm(request.POST, request.FILES)

        if not form.is_valid():
            data_context = {'upload_form':form, 'mapped_fields': LANGUAGE_CSV_FIELDS}
            return render(request,'upload-comments-csv-form.html', data_context)

        f = request.FILES['file']
        file_path = os.path.join(settings.BASE_DIR,'dictionary', 'upload') + '/' +request.user.username + '.' + f.name

        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        with open(file_path , 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        log_file_path = import_comments_csv(request, file_path)

        request.session['log_file_path'] = log_file_path

        form = UploadCSVForm()
        data_context = {'upload_form':form,'log_link':'download_log', 'mapped_fields': TAG_CSV_FIELDS}
        return render(request,'upload-comments-csv-form.html', data_context)

class UploadLanguageCSVView(View):

    def get(self, request):
        form = UploadCSVForm()
        data_context = {'upload_form':form, 'mapped_fields': LANGUAGE_CSV_FIELDS}
        return render(request,'upload-language-csv-form.html', data_context)

    def post(self, request):

        form = UploadCSVForm(request.POST, request.FILES)

        if not form.is_valid():
            data_context = {'upload_form':form, 'mapped_fields': LANGUAGE_CSV_FIELDS}
            return render(request,'upload-language-csv-form.html', data_context)

        f = request.FILES['file']
        file_path = os.path.join(settings.BASE_DIR,'dictionary', 'upload') + '/' +request.user.username + '.' + f.name

        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        with open(file_path , 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        log_file_path = import_language_csv(request, file_path)

        request.session['log_file_path'] = log_file_path

        form = UploadCSVForm()
        data_context = {'upload_form':form,'log_link':'download_log', 'mapped_fields': TAG_CSV_FIELDS}
        return render(request,'upload-language-csv-form.html', data_context)

class UploadTagCSVView(View):

    def get(self, request):
        form = UploadCSVForm()
        data_context = {'upload_form':form, 'mapped_fields': TAG_CSV_FIELDS}
        return render(request,'upload-tag-csv-form.html', data_context)

    def post(self, request):

        form = UploadCSVForm(request.POST, request.FILES)

        if not form.is_valid():
            data_context = {'upload_form':form, 'mapped_fields': TAG_CSV_FIELDS}
            return render(request,'upload-tag-csv-form.html', data_context)

        f = request.FILES['file']
        file_path = os.path.join(settings.BASE_DIR,'dictionary', 'upload') + '/' +request.user.username + '.' + f.name
        #pdb.set_trace()
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        with open(file_path , 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        log_file_path = import_tag_csv(request, file_path)

        request.session['log_file_path'] = log_file_path

        form = UploadCSVForm()
        data_context = {'upload_form':form,'log_link':'download_log', 'mapped_fields': TAG_CSV_FIELDS}
        return render(request,'upload-tag-csv-form.html', data_context)

class UploadCSVView(View):

    def get(self, request):
        print('upload-view')
        form = UploadCSVForm()
        data_context = {'upload_form':form, 'mapped_fields': DICTIONARY_CSV_FIELDS}
        return render(request,'upload-csv-form.html', data_context)

    def post(self, request):

        form = UploadCSVForm(request.POST, request.FILES)

        if not form.is_valid():
            data_context = {'upload_form':form, 'mapped_fields': DICTIONARY_CSV_FIELDS}
            return render(request,'upload-csv-form.html', data_context)

        f = request.FILES['file']
        file_path = os.path.join(settings.BASE_DIR,'dictionary', 'upload') + '/' +request.user.username + '.' + f.name

        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        with open(file_path , 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        #pdb.set_trace()

        thread = Thread(target=import_csv, args=(request, file_path, request.user,))
        thread.start()
        #log_file_path = import_csv(request, file_path, request.user)

        request.session['log_file_path'] = 'log_file_path'

        form = UploadCSVForm()
        data_context = {'upload_form':form,'log_link':'download_log', 'mapped_fields': DICTIONARY_CSV_FIELDS}
        return render(request,'upload-csv-form.html', data_context)


class DemoSearchFormView(TemplateView):
    template_name = "demo-search-form.html"

class SearchView(View):

    def get(self, request):

        request_context = RequestContext(request)
        return render(request,'search-form-get.html', data_context)

    def post(self, request):
        #pdb.set_trace()
        form = SearchForm(request.POST)

        form_valid = form.is_valid()
        cleaned_data = form.clean()

        word_entries = None

        #pdb.set_trace()
        if form_valid:

            keywords = cleaned_data['search_input'].split()
            q_obj = Q()
            for keyword in keywords:
                q_obj &= Q(word__icontains=keyword) | Q(short_description__icontains=keyword) | Q(word_content__content__icontains=keyword)

            #pdb.set_trace()
            word_entries = WordEntry.objects.filter(is_published=True).filter(q_obj)

        data_context = {'word_entries':word_entries}
        return render(request,'search-result.html', data_context)


class WordEntryView(View):

    def get(self, request, tags):

        tag_list = tags.split('/')
        #pdb.set_trace()
        if WordEntry.objects.filter(relative_url=tag_list[-1]).exists():

            word_entry = WordEntry.objects.get(relative_url=tag_list[-1])
            word_entry.access_count += 1
            word_entry.save()
            form_initial = {'word_entry_id': word_entry.id}
            #pdb.set_trace()
            if request.user.is_authenticated():
                form_initial['email'] = request.user.email
                form_initial['name'] = request.user.get_full_name()

            form = WordCommentForm(initial=form_initial)

            meta_data_locals = [
                {
                    'name':'description',
                    'content':word_entry.short_description
                },
                {
                    'property':'og:description',
                    'content':word_entry.short_description
                },
            ]

            data_context = {'word_entry':word_entry, 'title': word_entry.word,'comment_form':form, 'meta_data_locals': meta_data_locals , 'empty_image': NV_DICTIONARY_GALLERY_EMPTY_IMAGE, 'site_url': NV_SITE_URL, 'dictionary_url': NV_DICTIONARY_URL}

            return render(request,word_entry.template, data_context)

        #pdb.set_trace()

        if tag_list[0]!='':
            word_entries = WordEntry.objects.filter(is_published=True, tags__name__iexact=tag_list.pop(0))
            for tag in tag_list:
                word_entries = word_entries.filter(is_published=True, tags__name__iexact=tag)
        else:
            word_entries = WordEntry.objects.filter(is_published=True)

        data_context = {'word_entries':word_entries, 'site_url': NV_SITE_URL, 'dictionary_url': NV_DICTIONARY_URL}

        return render(request,'word-entries-tags.html', data_context)

    def post(self, request, tags):

        #pdb.set_trace()
        form = WordCommentForm(request.POST)
        form_valid = form.is_valid()
        cleaned_data = form.clean()

        word_entry = WordEntry.objects.get(id=cleaned_data['word_entry_id'])
        pdb.set_trace()
        if form_valid:

            comment = form.save()
            comment.author_ip = request.META['REMOTE_ADDR']

            comment.save()
            form = WordCommentForm(initial={'word_entry_id': word_entry.id})

        data_context = {'word_entry':word_entry,'comment_form':form, 'empty_image': NV_DICTIONARY_GALLERY_EMPTY_IMAGE, 'site_url': NV_SITE_URL, 'dictionary_url': NV_DICTIONARY_URL}

        return render(word_entry.template, data_context)
