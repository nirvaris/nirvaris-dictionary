from django.shortcuts import render

# Create your views here.

import pdb

from django.db.models import Q
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic.base import View
# Create your views here.

from .forms import CommentForm, SearchForm, UploadCSVForm
from .models import WordEntry

class UploadCSV(View):

    def get(self, request):

        form = UploadCSVForm()
        request_context = RequestContext(request,{'upload_form':form})
        return render_to_response('upload-csv-form.html', request_context)
        
    def post(self, request):

        form = UploadCSVForm(request.POST, request.FILES)

        if not form.is_valid():
            request_context = RequestContext(request,{'upload_form':form})
            return render_to_response('upload-csv-form.html', request_context)

        f = request.FILES['file']
        with open('upload/' + f.name , 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)


        form = UploadFileForm()
        request_context = RequestContext(request,{'upload_form':form})
        return render_to_response('upload-csv-form.html', request_context)

class SearchView(View):

    def post(self, request):
        form = SearchForm(request.POST)
        
        form_valid = form.is_valid()
        cleaned_data = form.clean()
        
        word_entries = None
        
        if form_valid:
            
            keywords = cleaned_data['search_input'].split()
            q_obj = Q()
            for keyword in keywords:
                q_obj &= Q(word_icontains=keyword) | Q(short_description_icontains=keyword) | Q(scientific_name_icontains=keyword) | Q(meaning_icontains=keyword) | Q(curiosities_icontains=keyword)
                
            word_entries = WordEntry.objects.all()

        request_context = RequestContext(request,{'word_entries':word_entries})
        return render_to_response('search-result.html', request_context)
        
    def get(self, request):

        form = SearchForm()
        request_context = RequestContext(request,{'search_form':form})
        return render_to_response('search-form.html', request_context)        

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
            
            request_context = RequestContext(request,{'word_entry':word_entry,'form':form})

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

        request_context = RequestContext(request,{'word_entry':word_entry,'form':form})

        return render_to_response(word_entry.template, request_context)