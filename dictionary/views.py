import os
import pdb

from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from django.views.generic import TemplateView

from django.utils.encoding import smart_str

from django.views.generic.base import View
# Create your views here.

from .csv_things import import_csv, import_tag_csv, import_language_csv, DICTIONARY_CSV_FIELDS, TAG_CSV_FIELDS, LANGUAGE_CSV_FIELDS
from .forms import CommentForm, SearchForm, UploadCSVForm
from .models import WordEntry

NV_DICTIONARY_GALLERY_EMPTY_IMAGE = 'static/image/empty-image.jpg'

if hasattr(settings, 'NV_THEME_GALLERY_EMPTY_IMAGE'):
    if settings.NV_THEME_GALLERY_EMPTY_IMAGE:
        NV_THEME_GALLERY_EMPTY_IMAGE = settings.NV_THEME_GALLERY_EMPTY_IMAGE

class DownloadImportLogView(View):

    def get(self, request):
        log_file = open(request.session['log_file_path'])
        #pdb.set_trace()
        response = HttpResponse(log_file, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('import-log.log.txt')

        return response

class UploadLanguageCSVView(View):

    def get(self, request):
        form = UploadCSVForm()
        request_context = RequestContext(request,{'upload_form':form, 'mapped_fields': LANGUAGE_CSV_FIELDS})
        return render_to_response('upload-language-csv-form.html', request_context)

    def post(self, request):

        form = UploadCSVForm(request.POST, request.FILES)

        if not form.is_valid():
            request_context = RequestContext(request,{'upload_form':form, 'mapped_fields': LANGUAGE_CSV_FIELDS})
            return render_to_response('upload-language-csv-form.html', request_context)

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
        request_context = RequestContext(request,{'upload_form':form,'log_link':'download_log', 'mapped_fields': TAG_CSV_FIELDS})
        return render_to_response('upload-language-csv-form.html', request_context)

class UploadTagCSVView(View):

    def get(self, request):
        form = UploadCSVForm()
        request_context = RequestContext(request,{'upload_form':form, 'mapped_fields': TAG_CSV_FIELDS})
        return render_to_response('upload-tag-csv-form.html', request_context)

    def post(self, request):

        form = UploadCSVForm(request.POST, request.FILES)

        if not form.is_valid():
            request_context = RequestContext(request,{'upload_form':form, 'mapped_fields': TAG_CSV_FIELDS})
            return render_to_response('upload-tag-csv-form.html', request_context)

        f = request.FILES['file']
        file_path = os.path.join(settings.BASE_DIR,'dictionary', 'upload') + '/' +request.user.username + '.' + f.name

        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        with open(file_path , 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        log_file_path = import_tag_csv(request, file_path)

        request.session['log_file_path'] = log_file_path

        form = UploadCSVForm()
        request_context = RequestContext(request,{'upload_form':form,'log_link':'download_log', 'mapped_fields': TAG_CSV_FIELDS})
        return render_to_response('upload-tag-csv-form.html', request_context)

class UploadCSVView(View):

    def get(self, request):
        form = UploadCSVForm()
        request_context = RequestContext(request,{'upload_form':form, 'mapped_fields': DICTIONARY_CSV_FIELDS})
        return render_to_response('upload-csv-form.html', request_context)

    def post(self, request):

        form = UploadCSVForm(request.POST, request.FILES)

        if not form.is_valid():
            request_context = RequestContext(request,{'upload_form':form, 'mapped_fields': DICTIONARY_CSV_FIELDS})
            return render_to_response('upload-csv-form.html', request_context)

        f = request.FILES['file']
        file_path = os.path.join(settings.BASE_DIR,'dictionary', 'upload') + '/' +request.user.username + '.' + f.name

        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        with open(file_path , 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        log_file_path = import_csv(request, file_path, request.user)

        request.session['log_file_path'] = log_file_path

        form = UploadCSVForm()
        request_context = RequestContext(request,{'upload_form':form,'log_link':'download_log', 'mapped_fields': DICTIONARY_CSV_FIELDS})
        return render_to_response('upload-csv-form.html', request_context)


class DemoSearchFormView(TemplateView):
    template_name = "demo-search-form.html"

class SearchView(View):

    def get(self, request):

        request_context = RequestContext(request)
        return render_to_response('search-form-get.html', request_context)

    def post(self, request):
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
            word_entries = WordEntry.objects.filter(q_obj)

        request_context = RequestContext(request,{'word_entries':word_entries})
        return render_to_response('search-result.html', request_context)


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

            form = CommentForm(initial=form_initial)

            request_context = RequestContext(request,{'word_entry':word_entry,'form':form, 'empty_image': NV_DICTIONARY_GALLERY_EMPTY_IMAGE})

            return render_to_response(word_entry.template, request_context)

        #pdb.set_trace()

        if tag_list[0]!='':
            word_entries = WordEntry.objects.filter(tags__name__iexact=tag_list.pop(0))
            for tag in tag_list:
                word_entries = word_entries.filter(tags__name__iexact=tag)
        else:
            word_entries = WordEntry.objects.all()

        request_context = RequestContext(request,{'word_entries':word_entries})

        return render_to_response('word-entries-tags.html', request_context)

    def post(self, request, tags):

        form = CommentForm(request.POST)

        form_valid = form.is_valid()
        cleaned_data = form.clean()

        word_entry = WordEntry.objects.get(id=cleaned_data['word_entry_id'])

        if form_valid:
            form.save()
            form = CommentForm(initial={'word_entry_id': word_entry_id.id})

        request_context = RequestContext(request,{'word_entry':word_entry,'form':form, 'empty_image': NV_DICTIONARY_GALLERY_EMPTY_IMAGE})

        return render_to_response(word_entry.template, request_context)
